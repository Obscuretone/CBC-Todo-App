import axios from 'axios';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const loginUser = async (email, password) => {
    const response = await axios.post(`${apiUrl}/auth`, { email, password });
    return response.data;
};

export const registerUser = async (username, email, password) => {
    const response = await axios.post(`${apiUrl}/auth/register`, { username, email, password });
    return response.data;
};
