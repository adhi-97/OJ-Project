import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000/', // Your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable this if you're dealing with cookies, sessions, or CSRF tokens
});

export default instance;
