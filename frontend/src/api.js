// src/api.js
import axios from 'axios';

// Get the base URL from the environment variable
const apiUrl = process.env.REACT_APP_API_URL;

// Function to login user using Azure AD token
export const loginUser = async (token) => {
    console.log("loginUser" + `${apiUrl}/auth/`)
    try {
        const response = await axios.post(`${apiUrl}/auth/`, {}, {
            headers: {
                Authorization: `Bearer ${token}`, // Send the token as a bearer token
            },
        });
        return response.data; // Return the response data
    } catch (error) {
        console.error("Login failed:", error);
        throw error;
    }
};
