// src/Router.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import ListProblems from './components/ListProblems';
import ViewProblem from './components/ViewProblem';

const AppRouter = () => (
  <Router>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register/>} />
      <Route path="/problems" element={<ListProblems/>} />
      <Route path="/problems/:id" element={<ViewProblem />} />
      {/* Add more routes here */}
    </Routes>
  </Router>
);

export default AppRouter;
