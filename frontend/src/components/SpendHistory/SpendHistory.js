import React, { useState, useEffect } from 'react';
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Collapse,
  CircularProgress,
  Box
} from '@mui/material';
import axios from 'axios';

const SpendHistory = () => {
  const [isHistoryVisible, setIsHistoryVisible] = useState(false);
  const [spendData, setSpendData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSpendHistory = async () => {
      try {
        const response = await axios.get('/api/spend-history');
        setSpendData(response.data);
      } catch (error) {
        console.error('Error fetching spend history:', error);
        // Mock data for development
        setSpendData([
          { date: '2024-07-01', description: 'Groceries', amount: 75.50 },
          { date: '2024-07-02', description: 'Gas', amount: 40.00 },
          { date: '2024-07-03', description: 'Dinner', amount: 60.25 },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchSpendHistory();
  }, []);

  const toggleHistoryVisibility = () => {
    setIsHistoryVisible(!isHistoryVisible);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="10vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <div>
      <Button variant="contained" onClick={toggleHistoryVisibility}>
        {isHistoryVisible ? 'Hide Spend History' : 'Show Spend History'}
      </Button>
      <Collapse in={isHistoryVisible}>
        <TableContainer component={Paper} style={{ marginTop: '20px' }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Amount</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {spendData.map((row) => (
                <TableRow key={row.date}>
                  <TableCell>{row.date}</TableCell>
                  <TableCell>{row.description}</TableCell>
                  <TableCell>${row.amount.toFixed(2)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Collapse>
    </div>
  );
};

export default SpendHistory;
