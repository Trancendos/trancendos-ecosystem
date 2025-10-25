import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  Box,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

const FinanceDashboard = () => {
    const [costs, setCosts] = useState([]);
    const [customerServices, setCustomerServices] = useState([]);
    const [loadingCosts, setLoadingCosts] = useState(true);
    const [loadingServices, setLoadingServices] = useState(true);
    const [newService, setNewService] = useState({ name: '', description: '', price: '' });

    useEffect(() => {
        fetchCosts();
        fetchCustomerServices();
    }, []);

    const fetchCosts = async () => {
        try {
            const response = await axios.get('/api/costs');
            setCosts(response.data);
        } catch (error) {
            console.error('Error fetching costs:', error);
        } finally {
            setLoadingCosts(false);
        }
    };

    const fetchCustomerServices = async () => {
        try {
            const response = await axios.get('/api/customer-services');
            setCustomerServices(response.data);
        } catch (error) {
            console.error('Error fetching customer services:', error);
        } finally {
            setLoadingServices(false);
        }
    };

    const handleApprove = async (id) => {
        try {
            await axios.post(`/api/costs/${id}/approve`);
            fetchCosts();
        } catch (error) {
            console.error('Error approving cost:', error);
        }
    };

    const handleReject = async (id) => {
        try {
            await axios.post(`/api/costs/${id}/reject`);
            fetchCosts();
        } catch (error) {
            console.error('Error rejecting cost:', error);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewService({ ...newService, [name]: value });
    };

    const handleAddService = async () => {
        try {
            await axios.post('/api/customer-services', newService);
            fetchCustomerServices();
            setNewService({ name: '', description: '', price: '' });
        } catch (error) {
            console.error('Error adding service:', error);
        }
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>Finance and Accountancy Dashboard</Typography>

            <Grid container spacing={4}>
                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h5" gutterBottom>Internal Cost Management</Typography>
                            {loadingCosts ? <CircularProgress /> : (
                                <TableContainer component={Paper}>
                                    <Table>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Service Name</TableCell>
                                                <TableCell>Details</TableCell>
                                                <TableCell>Status</TableCell>
                                                <TableCell>Actions</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {costs.map((cost) => (
                                                <TableRow key={cost.id}>
                                                    <TableCell>{cost.serviceName}</TableCell>
                                                    <TableCell>{cost.costDetails}</TableCell>
                                                    <TableCell>{cost.status}</TableCell>
                                                    <TableCell>
                                                        <Button variant="contained" color="success" onClick={() => handleApprove(cost.id)} disabled={cost.status !== 'PENDING'}>Approve</Button>
                                                        <Button variant="contained" color="error" onClick={() => handleReject(cost.id)} disabled={cost.status !== 'PENDING'}>Reject</Button>
                                                    </TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            )}
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h5" gutterBottom>Customer Services</Typography>
                            {loadingServices ? <CircularProgress /> : (
                                <TableContainer component={Paper}>
                                    <Table>
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Service Name</TableCell>
                                                <TableCell>Description</TableCell>
                                                <TableCell>Price</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {customerServices.map((service) => (
                                                <TableRow key={service.id}>
                                                    <TableCell>{service.name}</TableCell>
                                                    <TableCell>{service.description}</TableCell>
                                                    <TableCell>${service.price}</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            )}
                            <Box mt={2}>
                                <Typography variant="h6">Add New Service</Typography>
                                <TextField label="Name" name="name" value={newService.name} onChange={handleInputChange} fullWidth margin="normal" />
                                <TextField label="Description" name="description" value={newService.description} onChange={handleInputChange} fullWidth margin="normal" />
                                <TextField label="Price" name="price" value={newService.price} onChange={handleInputChange} fullWidth margin="normal" />
                                <Button variant="contained" onClick={handleAddService}>Add Service</Button>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Container>
    );
};

export default FinanceDashboard;
