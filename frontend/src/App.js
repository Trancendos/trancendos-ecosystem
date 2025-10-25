import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Auth/Login';
import TransactionList from './components/Transactions/TransactionList';
import AnalyticsDashboard from './components/Analytics/AnalyticsDashboard';
import FinanceDashboard from './components/FinanceDashboard/FinanceDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Trancendos Ecosystem
            </Typography>
          </Toolbar>
        </AppBar>
        
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/login" element={<Login />} />
            <Route path="/transactions" element={<TransactionList />} />
            <Route path="/analytics" element={<AnalyticsDashboard />} />
            <Route path="/finance" element={<FinanceDashboard />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
}

export default App;