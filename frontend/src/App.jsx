import { Navigate, Routes, Route } from 'react-router-dom';

import Header from './components/Header';
import Home from './components/Home';
import Login from './components/Login';
import TaskList from './components/TaskList';

function App() {
  const isAuthenticated = Boolean(localStorage.getItem('authToken'));

  return (
    <div id="app_wrapper">
      <Header />
      <div id="routes">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={isAuthenticated ? <Navigate to="/tasks" replace /> : <Login />} />
          <Route
            path="/tasks"
            element={isAuthenticated ? <TaskList /> : <Navigate to="/login" replace />}
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
