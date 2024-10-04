import React, { useEffect, useState } from "react";
import axios from "axios";
import { formatDistanceToNow } from "date-fns";
import { useNavigate } from "react-router-dom";
import './TaskList.css'; // Import CSS for animations

const TaskList = () => {
    const [tasks, setTasks] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const [newTask, setNewTask] = useState({ title: "", description: "" }); // State for new task

    const navigate = useNavigate();

    const apiUrl = process.env.REACT_APP_API_URL

    const ERROR_MESSAGES = {
        UNAUTHORIZED: "User is not authenticated",
        TOKEN_EXPIRED: "Token has expired. Please log in again.",
        FETCH_FAILED: "Failed to fetch tasks. Please try again.",
        CREATE_FAILED: "Failed to create task. Please try again.",
        DELETE_FAILED: "Failed to delete task. Please try again."
    };

    // Function to fetch tasks from the API
    const getTasks = async () => {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError(ERROR_MESSAGES.UNAUTHORIZED);
                setLoading(false);
                return;
            }

            const taskResponse = await axios.get(`${apiUrl}/tasks`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            setTasks(taskResponse.data.tasks); // Update the tasks state
            setError(null); // Clear any existing errors
        } catch (error) {
            console.error("Error fetching tasks:", error);
            if (error.response && error.response.status >= 400 && error.response.status < 500) {
                // Check if token is expired
                setError(ERROR_MESSAGES.TOKEN_EXPIRED);
                navigate("/login"); // Redirect to login page
            } else {
                setError(ERROR_MESSAGES.FETCH_FAILED);
            }
        } finally {
            setLoading(false); // Set loading to false once done
        }
    };

    // Function to create a new task
    const createTask = async (event) => {
        event.preventDefault(); // Prevent default form submission

        if (!newTask.title || !newTask.description) {
            setError("Both fields are required.");
            return; // Validate input
        }

        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError(ERROR_MESSAGES.UNAUTHORIZED);
                return;
            }

            // Make the POST request to create a new task
            const response = await axios.post(`${apiUrl}/tasks`, newTask, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            // Add the new task to the top of the task list
            setTasks(prevTasks => [response.data.task, ...prevTasks]);
            setNewTask({ title: '', description: '' }); // Clear the input fields
            setError(null); // Clear any existing errors
        } catch (error) {
            console.error("Error creating task:", error);
            setError(ERROR_MESSAGES.CREATE_FAILED);
        }
    };

    // Function to delete a task
    const deleteTask = async (uuid) => {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError(ERROR_MESSAGES.UNAUTHORIZED);
                return;
            }

            // Make the DELETE request to the API
            await axios.delete(`${apiUrl}/tasks/${uuid}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            // Mark the task as deleted and update its status
            setTasks(prevTasks => {
                const updatedTasks = prevTasks.map(task => {
                    if (task.uuid === uuid) {
                        return { ...task, deleted: true, status: "deleted" }; // Mark as deleted and update status
                    }
                    return task;
                });
                return updatedTasks;
            });

            setError(null); // Clear any existing errors
        } catch (error) {
            console.error("Error deleting task:", error);
            setError(ERROR_MESSAGES.DELETE_FAILED);
        }
    };

    // useEffect to fetch tasks on component mount
    useEffect(() => {
        getTasks();
    }, []);

    if (loading) {
        return <p>Loading tasks...</p>; // Display loading message
    }

    return (
        <div>
            <h1>Tasks
            </h1>


            {error && <p style={{ color: 'red' }}>{error}</p>}

            <form className="new-task" onSubmit={createTask} style={{ marginBottom: '20px' }}>
                <input
                    type="text"
                    placeholder="Task Title"
                    value={newTask.title}
                    onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                    required
                    style={{ marginRight: '10px' }}
                />
                <textarea
                    placeholder="Description"
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    required
                    style={{ width: '100%', height: '100px', marginBottom: '10px' }}
                />
                <button type="submit">Create Task</button>



            </form>
            <button id="refresh" onClick={getTasks}>
                ↻ refresh
            </button>


            {
                tasks.length > 0 ? (
                    <div>
                        <ul className="tasks">
                            {tasks.map((task) => {
                                const createdAt = new Date(task.created_at + "+0000"); // Assume created_at is in UTC
                                const isDeleted = task.deleted; // Check if task is marked as deleted
                                return (
                                    <li
                                        key={task.uuid}
                                        className={`task-item ${isDeleted ? 'deleted' : ''}`}
                                        style={{
                                            opacity: isDeleted ? 0.2 : 1, // Gray out deleted tasks
                                        }}
                                    >
                                        <h3 style={{ textDecoration: isDeleted ? 'line-through' : 'none' }}>{task.title}</h3> {/* Ensure we use task.title */}
                                        <p style={{ textDecoration: isDeleted ? 'line-through' : 'none' }}>{task.description}</p>
                                        <p className="task-status">Status: <span>{isDeleted ? "deleted" : task.status}</span></p> {/* Change status to "deleted" */}
                                        <p className="task-created">Created: {formatDistanceToNow(createdAt, { addSuffix: true })}</p>
                                        <button
                                            onClick={() => deleteTask(task.uuid)}
                                            disabled={isDeleted}
                                            style={{
                                                cursor: isDeleted ? 'not-allowed' : 'pointer',
                                                opacity: isDeleted ? 0.5 : 1 // Make delete button gray for deleted tasks
                                            }}
                                        >
                                            Complete
                                        </button>
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                ) : (
                    <p>No tasks available.</p>
                )
            }
        </div >
    );
};

export default TaskList;
