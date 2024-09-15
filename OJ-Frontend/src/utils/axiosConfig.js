import axios from 'axios';

// Create an instance of Axios
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  withCredentials: true, // This ensures cookies are sent with each request
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
