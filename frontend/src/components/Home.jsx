import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    const user = JSON.parse(localStorage.getItem('currentUser') || 'null');

    return (
        <main className="home-panel">
            <h1>CBC Todo App</h1>
            <p>A small full-stack task manager with a Sanic API, React frontend, MariaDB persistence, and architecture notes for a larger Azure deployment.</p>
            {user ? (
                <Link className="primary-link" to="/tasks">Open tasks</Link>
            ) : (
                <Link className="primary-link" to="/login">Log in or create an account</Link>
            )}
        </main>
    );
};

export default Home;
