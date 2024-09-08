import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import './ViewProblem.css'; // Import the separate CSS file
import { getCSRFToken } from '../utils/csrfUtils'; 

const CodeSubmissionApp = () => {
  const { id: problemId } = useParams(); // Extract problemId from URL parameters
  const [code, setCode] = useState('# write your code here');
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [problemStatement, setProblemStatement] = useState('');
  const [problemTitle, setProblemTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState('python'); // State for selected language
  const [testResults, setTestResults] = useState([]);

  // Fetch the problem statement from the backend API
  useEffect(() => {
    const fetchProblemDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/home/problems/${problemId}/`, {
          method: 'GET',
          credentials: 'include', // Include credentials to handle CSRF
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch problem details');
        }

        const data = await response.json();
        setProblemStatement(data.statement);
        setProblemTitle(data.name);

      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProblemDetails();
    if(language=='cpp')
      setCode("// write your code here");
    if(language=='python')
      setCode("# write your code here");
  }, [problemId,language]);

  if (loading) return <p>Loading problem statement...</p>;
  if (error) return <p>Error: {error}</p>;


  const handleSubmit = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/codeSubmission/problem/submit-code-test/', {
        method: 'POST',
        credentials: 'include', // Include credentials to handle CSRF
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ language, code, input_data: input ,problem_id:problemId}), // Include selected language
      });
      
      if (!response.ok) {
        throw new Error('Failed to submit code');
      }

      const result = await response.json();
      if (result.success) {
        setOutput('All test cases passed!');
      } else {
        
        setTestResults(result.output_data); // Assuming this is an array of test case results
        // Format the output for display
      const formattedOutput = result.output_data.map(
        (testResult) =>
          `Test Case ${testResult.test_case}: ${
            testResult.success ? 'Passed' : 'Failed'
          }`
      ).join('\n');

      setOutput('Some test cases failed:\n'+formattedOutput); // Set the formatted output
      }
    } catch (error) {
      console.error('Error submitting code:', error);
      setError('Failed to submit code');
    }
  };

  const handleRun = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/codeSubmission/problem/submit-code/', {
        method: 'POST',
        credentials: 'include', // Include credentials to handle CSRF
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ language, code, input_data: input }), // Include selected language
      });
      
      if (!response.ok) {
        throw new Error('Failed to submit code');
      }

      const result = await response.json();
      setOutput(result.output_data);
    } catch (error) {
      console.error('Error submitting code:', error);
    }
  };

  return (
    <div className="container1">
      <div className="flex h-full">
        {/* Problem Statement Panel */}
        <div className="problem-statement">
          <h2 className="text-lg font-bold mb-2">Problem Statement</h2>
          <p className="text-sm">{problemStatement}</p>
        </div>

        {/* Code Editor */}
        <div className="code-editor">
          <Editor
            height="60vh"
            defaultLanguage={language}
            value={code}
            onChange={setCode}
            theme="vs-dark"
            options={{
              fontSize: 14,
              automaticLayout: true,
              minimap: { enabled: false },
            }}
          />
        </div>
      </div>

      {/* Language Selection Dropdown */}
      <div className="language-dropdown">
        <label htmlFor="language" className="font-semibold mr-2">Select Language:</label>
        <select
          id="language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="language-select"
        >
          <option value="python">Python</option>
          <option value="cpp">C++</option>
          {/* Add more languages as needed */}
        </select>
      </div>

      {/* Input and Output Area */}
      <div className="flex mt-4">
        <div className="input-output-area">
          <h3 className="font-semibold mb-2">Input</h3>
          <textarea
            className="input-output-textarea"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter input here..."
          />
        </div>
        <div className="input-output-area">
          <h3 className="font-semibold mb-2">Output</h3>
          <textarea
            className="input-output-textarea"
            value={output}
            readOnly
            placeholder="Output will appear here..."
          />
        </div>
        
        {/* Run Button */}
        <div className="run-button-container">
          <button
            onClick={handleRun}
            className="run-button"
          >
            Run
          </button>
        </div>

        {/* Submit Button */}
        <div className="submit-button-container">
          <button
            onClick={handleSubmit}
            className="submit-button"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};

export default CodeSubmissionApp;
