import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import PrivateRoute from './components/auth/PrivateRoute';
import Layout from './components/layout/Layout';
import { AuthProvider } from './contexts/AuthContext';
import Dashboard from './pages/Dashboard';
import Diagnosis from './pages/Diagnosis';
import Emergency from './pages/Emergency';
import Login from './pages/Login';
import PatientDetails from './pages/PatientDetails';
import PatientList from './pages/PatientList';
import Radiology from './pages/Radiology';
import Specialists from './pages/Specialists';
import { theme } from './theme';

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route
                path="/"
                element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                }
              />
              <Route
                path="/patients"
                element={
                  <PrivateRoute>
                    <PatientList />
                  </PrivateRoute>
                }
              />
              <Route
                path="/patients/:id"
                element={
                  <PrivateRoute>
                    <PatientDetails />
                  </PrivateRoute>
                }
              />
              <Route
                path="/diagnosis"
                element={
                  <PrivateRoute>
                    <Diagnosis />
                  </PrivateRoute>
                }
              />
              <Route
                path="/radiology"
                element={
                  <PrivateRoute>
                    <Radiology />
                  </PrivateRoute>
                }
              />
              <Route
                path="/emergency"
                element={
                  <PrivateRoute>
                    <Emergency />
                  </PrivateRoute>
                }
              />
              <Route
                path="/specialists"
                element={
                  <PrivateRoute>
                    <Specialists />
                  </PrivateRoute>
                }
              />
            </Routes>
          </Layout>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App; 