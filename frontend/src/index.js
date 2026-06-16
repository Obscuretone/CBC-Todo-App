// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client'; // Use 'react-dom/client' for React 18
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { MsalProvider } from '@azure/msal-react'; // Only import from msal-react
import { PublicClientApplication } from '@azure/msal-browser'; // Correct import from msal-browser
import { msalConfig } from './config/authConfig'; // Ensure this path is correct
import './index.css'; // Importing the global styles

// Create an instance of the PublicClientApplication
const msalInstance = new PublicClientApplication(msalConfig);

// Create the root using createRoot
const root = ReactDOM.createRoot(document.getElementById('root')); // Use createRoot method

// Render the application
root.render(
  <React.StrictMode>
    <MsalProvider instance={msalInstance}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </MsalProvider>
  </React.StrictMode>
);
