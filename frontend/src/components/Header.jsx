import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.css';

const Header = () => {
    const navigate = useNavigate();
    const isAuthenticated = Boolean(localStorage.getItem('authToken'));

    const logout = () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
        navigate('/login');
    };

    return (
        <header className="app-header">
            <h1>CBC Todo</h1>
            <nav>
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/tasks">Tasks</Link></li>
                    <li>
                        {isAuthenticated ? (
                            <button className="nav-button" onClick={logout} type="button">Log out</button>
                        ) : (
                            <Link to="/login">Log in</Link>
                        )}
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
