import axios from 'axios';
import { getCSRFToken } from '../utils/csrfUtils';

// Create an instance of Axios
const axiosInstance = axios.create({
  baseURL: 'https://onlinejudge-oj.onrender.com/',
  withCredentials: true, // This ensures cookies are sent with each request
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken':getCSRFToken()
  },
});

// Interceptor to set CSRF token from cookies
axiosInstance.interceptors.request.use(
  async (config) => {
    // Assuming CSRF token is stored in cookies
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken'))
      ?.split('=')[1];

    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    console.log('Token--->'+csrfToken)
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
