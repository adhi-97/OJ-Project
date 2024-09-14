import axios from 'axios';
import { getCSRFToken } from '../utils/csrfUtils';

const instance = axios.create({
  baseURL: 'https://onlinejudge-oj.onrender.com/', // Your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable this if you're dealing with cookies, sessions, or CSRF tokens
});

// Add CSRF token to headers for every request
instance.interceptors.request.use(config => {
  const csrfToken = getCSRFToken();
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

export default instance;
