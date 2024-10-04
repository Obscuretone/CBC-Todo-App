import React, { useState } from 'react';
import { useMsal } from '@azure/msal-react';
import { loginUser } from '../api'; // Import the loginUser function
import { useNavigate } from 'react-router-dom'; // Import useNavigate


const Login = () => {
    const { instance } = useMsal();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [token, setToken] = useState(null); // Store the backend token
    const navigate = useNavigate(); // Initialize useNavigate
    const apiUrl = process.env.REACT_APP_API_URL


    const login = async () => {
        if (isLoading) return;

        setIsLoading(true);
        setError(null); // Reset any previous errors

        const loginRequest = {
            scopes: ["openid", "profile"], // Define the scopes you want
        };

        try {
            console.log("Attempting to login...");

            // Await loginPopup to complete before proceeding
            await instance.loginPopup(loginRequest);
            console.log("Login successful");

            // Now you can call acquireTokenPopup
            const tokenRequest = {
                scopes: ["user.read"], // Define the scopes you want for the token
            };

            console.log("Attempting to acquire token...");
            const response = await instance.acquireTokenPopup(tokenRequest);
            console.log("Token acquired:", response.accessToken);

            console.log("Calling API!")
            // Make a request to your backend /login endpoint
            const apiResponse = await loginUser(response.accessToken); // Use the loginUser function

            console.log("Response from backend:", apiResponse);

            if (apiResponse.token) {
                // Save the token in localStorage or sessionStorage for later use
                localStorage.setItem("authToken", apiResponse.token);
                setToken(apiResponse.token); // Update state with the token

                // Redirect user or update UI after successful login
                console.log("Authenticated successfully. Token saved.");

                navigate('/tasks'); // Redirect to /tasks

            } else {
                setError("Failed to retrieve token from backend.");
            }

        } catch (err) {
            console.error("Login failed:", err);
            setError("Login failed. Please try again.");
        } finally {
            setIsLoading(false); // Reset loading state regardless of success or failure
        }
    };

    const retryLogin = () => {
        setError(null); // Clear the error message
        login(); // Retry the login
    };

    return (
        <div>
            <h2>Login</h2>
            <button onClick={login} disabled={isLoading}>
                {isLoading ? "Logging in..." : "Login"}
            </button>
            {error && (
                <div>
                    <p style={{ color: 'red' }}>{error}</p>
                    <button onClick={retryLogin}>Retry</button>
                </div>
            )}
            {token && (
                <div>
                    <p style={{ color: 'green' }}>Authenticated! Token saved.</p>
                </div>
            )}
        </div>
    );
};

export default Login;
