import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, registerUser } from '../api';

const emptyForm = {
    username: '',
    email: '',
    password: '',
};

const Login = () => {
    const [mode, setMode] = useState('login');
    const [form, setForm] = useState(emptyForm);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const updateForm = (event) => {
        setForm({
            ...form,
            [event.target.name]: event.target.value,
        });
    };

    const submit = async (event) => {
        event.preventDefault();
        setIsLoading(true);
        setError(null);

        try {
            const response = mode === 'register'
                ? await registerUser(form.username, form.email, form.password)
                : await loginUser(form.email, form.password);

            localStorage.setItem('authToken', response.token);
            localStorage.setItem('currentUser', JSON.stringify(response.user));
            navigate('/tasks');
        } catch (err) {
            const message = err.response?.data?.error || 'Authentication failed. Check your details and try again.';
            setError(message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="auth-panel">
            <h1>{mode === 'register' ? 'Create an account' : 'Log in'}</h1>
            <form onSubmit={submit}>
                {mode === 'register' && (
                    <label>
                        Name
                        <input
                            autoComplete="name"
                            name="username"
                            onChange={updateForm}
                            required
                            type="text"
                            value={form.username}
                        />
                    </label>
                )}
                <label>
                    Email
                    <input
                        autoComplete="email"
                        name="email"
                        onChange={updateForm}
                        required
                        type="email"
                        value={form.email}
                    />
                </label>
                <label>
                    Password
                    <input
                        autoComplete={mode === 'register' ? 'new-password' : 'current-password'}
                        name="password"
                        onChange={updateForm}
                        required
                        type="password"
                        value={form.password}
                    />
                </label>
                {error && <p className="form-error">{error}</p>}
                <button disabled={isLoading} type="submit">
                    {isLoading ? 'Working...' : mode === 'register' ? 'Create account' : 'Log in'}
                </button>
            </form>
            <button
                className="link-button"
                onClick={() => {
                    setError(null);
                    setMode(mode === 'register' ? 'login' : 'register');
                }}
                type="button"
            >
                {mode === 'register' ? 'Use an existing account' : 'Create a new account'}
            </button>
        </main>
    );
};

export default Login;
