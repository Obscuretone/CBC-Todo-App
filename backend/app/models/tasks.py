import uuid
from sanic import Blueprint
from sanic.response import json
from sanic_openapi import doc  # For API documentation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from config import Config
from db import get_db_session
from redis_cache import get_redis_connection
import json as py_json
from datetime import datetime

task_blueprint = Blueprint("tasks", url_prefix="/tasks")


def is_valid_uuid(uuid_string):
    try:
        uuid_obj = uuid.UUID(uuid_string)  # Specify version to check against
        # Ensure the string matches the UUID representation
        return str(uuid_obj) == str(uuid_string)

    except ValueError:
        return False


# POST operation for creating a new task
@task_blueprint.route("/", methods=["POST"], name="Create Task")
@doc.summary("Create a new task")
@doc.description(
    "Create a new task with a title, an optional description, and a pending status."
)
@doc.tag("Tasks")
@doc.operation("create_task")
@doc.consumes(
    doc.JsonBody(
        {
            "title": doc.String(description="The title of the task", required=True),
            "description": doc.String(
                description="The description of the task (optional)", required=False
            ),
        }
    ),
    location="body",
    required=True,
)
@doc.response(
    200,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Task created"},
                    "task": {
                        "type": "object",
                        "properties": {
                            "uuid": {"type": "string", "example": "uuid_of_task"},
                            "title": {"type": "string", "example": "Sample Task"},
                            "description": {
                                "type": "string",
                                "example": "This is an optional description",
                            },
                            "status": {"type": "string", "example": "pending"},
                            "created_at": {"type": "string", "format": "date-time"},
                        },
                    },
                },
            }
        }
    },
)
@doc.response(
    500,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Task creation failed"},
                    "details": {"type": "string", "example": "Error message"},
                },
            }
        }
    },
)
async def create_task(request):
    redis = await get_redis_connection()
    user_uuid = request.ctx.user_uuid

    try:
        task_data = request.json
        title = task_data.get("title")
        description = task_data.get("description", None)
        status = "created"  # Status is always 'created' for new tasks created by API.
        task_uuid = str(uuid.uuid4())  # Generate a new UUID for the task

        # Debugging output
        print(
            f"Title: {title}, Description: {description}, Status: {status}, uuid: {task_uuid}"
        )

        task = {
            "uuid": task_uuid,
            "title": title,
            "description": description,
            "status": status,
            "user_uuid": user_uuid,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }
        try:
            # Prepare SQL for inserting the new task, ensuring 'status' is passed as a valid string
            AsyncSessionLocal = get_db_session()
            async with AsyncSessionLocal() as session:
                await session.execute(
                    text(
                        "INSERT INTO tasks (id, title, description, status, user_uuid, created_at) "
                        "VALUES (:uuid, :title, :description, :status, :user_uuid, :created_at)"
                    ),
                    task,
                )
                await session.commit()
        except Exception as e:
            print(e)
            return json({"message": "Task not created"}, status=500)

        await redis.delete("tasks_{user_uuid}")
        return json({"message": "Task created successfully", "task": task}, status=201)

    except Exception as e:
        return json({"error": "Task creation failed", "details": str(e)}, status=500)


@task_blueprint.route("/<task_id>", methods=["DELETE"], name="Delete Task")
@doc.summary("Delete a specific task")
@doc.description("Delete a task by its ID.")
@doc.tag("Tasks")
@doc.operation("delete_task")
@doc.response(
    200,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Task deleted"},
                },
            }
        }
    },
)
@doc.response(
    404,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Task not found"},
                },
            }
        }
    },
)
@doc.response(
    500,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Task deletion failed"},
                    "details": {"type": "string", "example": "Error message"},
                },
            }
        }
    },
)
async def delete_task(request, task_id):
    redis = await get_redis_connection()
    user_uuid = request.ctx.user_uuid

    try:
        print(task_id)
        if not is_valid_uuid(task_id):

            return json({"error": "{task_id} is an invalid UUID"}, status=400)

        # Check if the task exists
        AsyncSessionLocal = get_db_session()
        async with AsyncSessionLocal() as session:
            # Delete the task
            await session.execute(
                text(
                    "DELETE FROM tasks WHERE id = :task_id and user_uuid = :user_uuid"
                ),
                {"task_id": task_id, "user_uuid": request.ctx.user_uuid},
            )
            await session.commit()
            await redis.delete("tasks_{user_uuid}")
        return json({"message": "Task deleted"}, status=200)

    except Exception as e:
        return json({"error": "Task deletion failed", "details": str(e)}, status=500)


# GET operation for retrieving all tasks
@task_blueprint.route("/", methods=["GET"], name="Get all Tasks")
@doc.summary("Get all tasks")
@doc.description(
    "Fetch all tasks. First checks Redis cache, then queries the database if not cached."
)
@doc.tag("Tasks")
@doc.operation("get_all_tasks")
@doc.response(
    200,
    {
        "application/json": {
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "task": {"type": "string", "example": "Buy groceries"},
                    },
                },
            }
        }
    },
)
@doc.response(
    500,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Failed to retrieve tasks"},
                    "details": {"type": "string", "example": "Error message"},
                },
            }
        }
    },
)
async def get_all_tasks(request):
    redis = await get_redis_connection()

    user_uuid = request.ctx.user_uuid

    # Check if tasks are cached in Redis
    try:
        cached_tasks = await redis.get("tasks_{user_uuid}")
        if cached_tasks:
            print("Got cached tasks")
            return json({"tasks": py_json.loads(cached_tasks)}, status=200)
    except Exception as e:
        print("Could not get tasks from Redis")
        print(e)

    try:
        # If not cached, query the database for all tasks
        AsyncSessionLocal = get_db_session()
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text(
                    "SELECT * FROM tasks WHERE user_uuid = :user_uuid ORDER BY created_at desc;"
                ),
                {"user_uuid": request.ctx.user_uuid},
            )
            tasks = result.fetchall()  # This returns a list of Row objects
    except Exception as e:
        print("Could not get tasks from DB")
        print(e)

    # Convert SQLAlchemy Row objects (tuples) to dictionaries
    tasks_dict = [
        {
            "uuid": task[0],
            "title": task[1],
            "description": task[2],
            "status": task[3],
            "created_at": (
                task[4].isoformat() if task[4] else None
            ),  # Convert datetime to ISO format
        }
        for task in tasks
    ]

    # Cache the tasks in Redis
    await redis.set(
        "tasks_{user_uuid}", py_json.dumps(tasks_dict), ex=10
    )  # TODO: Make that longer

    return json({"tasks": tasks_dict}, status=200)
