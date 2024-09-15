import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getCSRFToken } from '../utils/csrfUtils'; // Import the helper function to get CSRF token
import './ListProblems.css'; // Import the CSS file
import axiosInstance from '../utils/axiosConfig'; 

function ListProblems() {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await axiosInstance.get('/home/problems/');
  
        if (!response.data) {
          throw new Error('Failed to fetch problems');
        }
  
        setProblems(response.data.all_problems); // Update to match API response structure
  
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
  
    fetchProblems();
  }, []);  

  if (loading) return <p>Loading problems...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="container">
      <h1 className="header">Problems List</h1>
      <ul>
        {problems.map((problem) => (
          <li
            key={problem.id}
            className="problem-item"
          >
            <div>
              <h2 className="problem-title">{problem.name}</h2>
              <p className="problem-difficulty">Difficulty: {problem.difficulty}</p>
            </div>
            <Link
              to={`/problems/${problem.id}`}
              className="view-details-link"
            >
              <span>SOLVE</span>
              <svg
                stroke="currentColor"
                strokeWidth="1"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
                  strokeLinejoin="round"
                  strokeLinecap="round"
                />
              </svg>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ListProblems;
