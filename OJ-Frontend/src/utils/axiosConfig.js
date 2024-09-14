import axios from 'axios';
import { getCSRFToken } from '../utils/csrfUtils'; 

const instance = axios.create({
  baseURL: 'https://onlinejudge-oj.onrender.com/', // Your backend URL
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': getCSRFToken(),
  },
  withCredentials: true, //  Enable this if you're dealing with cookies, sessions, or CSRF tokens
});

export default instance;
