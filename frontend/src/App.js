// src/App.js
import { Routes, Route } from 'react-router-dom';
import { useIsAuthenticated } from '@azure/msal-react';

import Header from './components/Header'; // Import your header component
import Home from './components/Home';
import Login from './components/Login';
import TaskList from './components/TaskList';

function App() {
  const isAuthenticated = useIsAuthenticated();

  return (

    <div id="app_wrapper">
      <Header />

      <div id="routes">
        <Routes>
          <Route path="/" element={<Home />} /> {/* Home route */}
          <Route path="/login" element={<Login />} /> {/* Login route */}
          <Route
            path="/tasks"
            element={isAuthenticated ? <TaskList /> : <Login />}
          /> {/* Protected tasks route */}
        </Routes>
      </div>
    </div>
  );
}

export default App;
