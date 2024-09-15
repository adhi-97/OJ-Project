import axios from 'axios';

// Create an instance of Axios
const axiosInstance = axios.create({
  baseURL: 'https://onlinejudge-oj.onrender.com/',
  withCredentials: true, // This ensures cookies are sent with each request
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
