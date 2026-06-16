import React, { useEffect, useState } from "react";
import axios from "axios";
import { formatDistanceToNow } from "date-fns";
import { useNavigate } from "react-router-dom";
import './TaskList.css';

const TaskList = () => {
    const [tasks, setTasks] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const [newTask, setNewTask] = useState({ title: "", description: "" });

    const navigate = useNavigate();

    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    const ERROR_MESSAGES = {
        UNAUTHORIZED: "User is not authenticated",
        TOKEN_EXPIRED: "Token has expired. Please log in again.",
        FETCH_FAILED: "Failed to fetch tasks. Please try again.",
        CREATE_FAILED: "Failed to create task. Please try again.",
        DELETE_FAILED: "Failed to delete task. Please try again."
    };

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

            setTasks(taskResponse.data.tasks);
            setError(null);
        } catch (error) {
            console.error("Error fetching tasks:", error);
            if (error.response && error.response.status >= 400 && error.response.status < 500) {
                setError(ERROR_MESSAGES.TOKEN_EXPIRED);
                localStorage.removeItem('authToken');
                localStorage.removeItem('currentUser');
                navigate("/login");
            } else {
                setError(ERROR_MESSAGES.FETCH_FAILED);
            }
        } finally {
            setLoading(false);
        }
    };

    const createTask = async (event) => {
        event.preventDefault();

        if (!newTask.title || !newTask.description) {
            setError("Both fields are required.");
            return;
        }

        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError(ERROR_MESSAGES.UNAUTHORIZED);
                return;
            }

            const response = await axios.post(`${apiUrl}/tasks`, newTask, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            setTasks(prevTasks => [response.data.task, ...prevTasks]);
            setNewTask({ title: '', description: '' });
            setError(null);
        } catch (error) {
            console.error("Error creating task:", error);
            setError(ERROR_MESSAGES.CREATE_FAILED);
        }
    };

    const deleteTask = async (uuid) => {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                setError(ERROR_MESSAGES.UNAUTHORIZED);
                return;
            }

            await axios.delete(`${apiUrl}/tasks/${uuid}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            setTasks(prevTasks => prevTasks.filter(task => task.uuid !== uuid));

            setError(null);
        } catch (error) {
            console.error("Error deleting task:", error);
            setError(ERROR_MESSAGES.DELETE_FAILED);
        }
    };

    useEffect(() => {
        getTasks();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    if (loading) {
        return <p>Loading tasks...</p>;
    }

    return (
        <div>
            <h1>Tasks</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            <form className="new-task" onSubmit={createTask}>
                <input
                    type="text"
                    placeholder="Task Title"
                    value={newTask.title}
                    onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                    required
                />
                <textarea
                    placeholder="Description"
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    required
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
                                const createdAt = new Date(task.created_at);
                                return (
                                    <li
                                        key={task.uuid}
                                        className="task-item"
                                    >
                                        <h3>{task.title}</h3>
                                        <p>{task.description}</p>
                                        <p className="task-status">Status: <span>{task.status}</span></p>
                                        <p className="task-created">Created: {formatDistanceToNow(createdAt, { addSuffix: true })}</p>
                                        <button
                                            onClick={() => deleteTask(task.uuid)}
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
