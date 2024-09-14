import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://onlinejudge-oj.onrender.com/', // Your backend URL
  headers: {
    'Content-Type': 'application/json',
    'Referer':'https://codexpert-vomp.onrender.com',
  },
  withCredentials: true, // Enable this if you're dealing with cookies, sessions, or CSRF tokens
});

export default instance;
