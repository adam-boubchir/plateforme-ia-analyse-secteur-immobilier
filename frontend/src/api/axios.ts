import axios from "axios";

export const API_BASE_URL = "http://localhost:8000";

export const API_URL = `${API_BASE_URL}/api/v1`;

const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

export default api;