import React from 'react';

function Leaderboard() {
  const rankings = [
    { id: 1, username: 'User1', total_points: 100 },
    { id: 2, username: 'User2', total_points: 90 },
    // Add more rankings here
  ];

  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Leaderboard</h2>
      <table className="w-full text-left">
        <thead>
          <tr>
            <th className="border-b-2 p-2">Username</th>
            <th className="border-b-2 p-2">Total Points</th>
          </tr>
        </thead>
        <tbody>
          {rankings.map((ranking) => (
            <tr key={ranking.id}>
              <td className="border-b p-2">{ranking.username}</td>
              <td className="border-b p-2">{ranking.total_points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
