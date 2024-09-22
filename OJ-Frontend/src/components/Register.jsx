import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import log from '../logger';
import './Login.css'; // Ensure the correct CSS file name
import axiosInstance from '../utils/axiosConfig';
const CreateUser = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirm_password, setCPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleCreateUser = async (event) => {
    event.preventDefault();
    try {
      const response = await axiosInstance.post('auth/register/', {
        "username":username,
        "password":password,
        "cpassword":confirm_password,
      });
      console.log('User created successfully:', response.data);
      // Navigate to another page if needed
      if(response.data.error){
        setError(''+error);
      }else{
        navigate('/'); // Change '/success' to your desired route
      }
    } catch (error) {
      log.error('There was an error creating the user:', error);
      console.log('Errors');
      if (error.response && error.response.data && error.response.data.error) {
        setError(error.response.data.error);
    } else {
        setError(''+error);
    }
    }
  };

  return (
    <div className="welcome-screen">
      <div className="welcome-message">
        <h1><span className="text-blue-500"><span className="text-red-500">C</span>ode - <span className="text-red-500">C</span>ompete - <span className="text-red-500">C</span>onquer</span></h1>
      </div>
      <div className="form-container">
        <p className="title">CodeXpert</p>
        <form className="form" onSubmit={handleCreateUser}>
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
            <div>
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
            </div>
            <div>
            <label htmlFor="confirm_password">Confirm Password</label>
            <input
              type="password"
              name="confirm password"
              id="confirm_password"
              required
              value={confirm_password}
              onChange={(e) => setCPassword(e.target.value)}
              className="w-full p-3 text-gray-900 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            </div>
          </div>
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="sign w-full bg-green-500 text-white p-3 rounded-lg hover:bg-green-600">
            Sign Up
          </button>
        </form>
        <br/>
        <p className="signup">Already have an account? <a href="/">Login</a>
        </p>
      </div>
    </div>
  );
};

export default CreateUser;
