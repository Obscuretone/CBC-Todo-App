from sanic import Sanic, response
from sanic_cors import CORS
import os
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from tortoise import Tortoise
from services.task_service import TaskService
from services.user_service import UserService
from middleware.auth import auth_middleware

from config import Config

app = Sanic("cbc-todo-api")

CORS_URL = os.environ.get("CORS_ORIGIN", "http://localhost:3000")
CORS(app, origins=[CORS_URL], supports_credentials=True, automatic_options=True)
app.register_middleware(auth_middleware, "request")


@app.route("/", methods=["GET"])
async def hello_world(request):
    return response.json({"message": "TODO API", "version": "1.0.0"})


@app.listener("before_server_start")
async def setup_services(app, loop):
    await Tortoise.init(
        db_url=Config.DATABASE_URL,
        modules={"models": ["models.Task", "models.User"]},
    )
    await Tortoise.generate_schemas()

    user_service = UserService()
    task_service = TaskService()

    UserController(app, user_service)
    TaskController(app, task_service)


@app.listener("after_server_stop")
async def cleanup_services(app, loop):
    # Close database connections after the server stops
    await Tortoise.close_connections()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=Config.SANIC_DEBUG,
        auto_reload=Config.SANIC_AUTO_RELOAD,
    )
