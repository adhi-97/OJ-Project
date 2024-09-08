import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import ListProblems from './components/ListProblems';
import ViewProblem from './components/ViewProblem';
import Leaderboard from './components/Leaderboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 p-4">
        <header className="bg-white shadow p-4 mb-6">
          <h1 className="text-2xl font-bold text-center">Online Judge</h1>
        </header>
        <main>
          <div className="container mx-auto">
            <Routes>
              <Route path="/" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/problems" element={<ListProblems />} />
              <Route path="/problems/:id" element={<ViewProblem />} />
              <Route path="/leaderboard" element={<Leaderboard />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;

