import React, { useState,useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import log from '../logger';
import { getFirstCSRFToken } from '../utils/csrfUtils';
import axiosInstance from '../utils/axiosConfig';

const LoginUser = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [csrfToken, setCsrfToken] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the CSRF token when the component mounts
    const fetchCSRFToken = async () => {
      const token = await getFirstCSRFToken();
      setCsrfToken(token);
    };

    fetchCSRFToken();
  }, []);

  const handleLoginUser = async (event) => {
    event.preventDefault();
    var response=null;
    
    try {
      response = await axiosInstance.post('auth/login/', {
        "username":username,
        "password":password,
      }, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        }
      });
      console.log('User Login successfull:', response.data);
      // Navigate to another page if needed
      navigate('/problems'); // Change '/success' to your desired route
    } catch (error) {
      log.error('There was an error logging in the user:', error);
      setError('Incorrect Username or Password');
    }
  };

  return (
    <div className="welcome-screen">
      <div className="welcome-message">
        <h1><span className="text-blue-500"><span className="text-red-500">C</span>ode - <span className="text-red-500">C</span>ompete - <span className="text-red-500">C</span>onquer</span></h1>
      </div>
      <div className="form-container">
        <p className="title">CodeXpert</p>
        <form className="form" onSubmit={handleLoginUser}>
          <div className="input-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              name="username"
              id="username"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-3 text-gray-900 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password"
              id="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-3 text-gray-900 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="forgot">
              <a href="#">Forgot Password?</a>
            </div>
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="sign w-full bg-green-500 text-white p-3 rounded-lg hover:bg-green-600">
            Sign in
          </button>
        </form>
        <br/>
        <p className="signup">Don't have an account?<a href="/register">Sign Up</a>
        </p>
      </div>
    </div>
  );
};

export default LoginUser;
