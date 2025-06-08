import {
    LocalHospital as DiagnosisIcon,
    Emergency as EmergencyIcon,
    People as PeopleIcon,
    Radiology as RadiologyIcon,
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Card,
    CardContent,
    CircularProgress,
    Grid,
    Typography,
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

interface DashboardStats {
  totalPatients: number;
  activeDiagnoses: number;
  pendingRadiology: number;
  activeEmergencies: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        // TODO: Replace with actual API call
        const response = await apiService.getPatients();
        setStats({
          totalPatients: response.length,
          activeDiagnoses: 0,
          pendingRadiology: 0,
          activeEmergencies: 0,
        });
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box mt={3}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  const statCards = [
    {
      title: 'Total Patients',
      value: stats?.totalPatients || 0,
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      color: '#1976d2',
    },
    {
      title: 'Active Diagnoses',
      value: stats?.activeDiagnoses || 0,
      icon: <DiagnosisIcon sx={{ fontSize: 40 }} />,
      color: '#2e7d32',
    },
    {
      title: 'Pending Radiology',
      value: stats?.pendingRadiology || 0,
      icon: <RadiologyIcon sx={{ fontSize: 40 }} />,
      color: '#ed6c02',
    },
    {
      title: 'Active Emergencies',
      value: stats?.activeEmergencies || 0,
      icon: <EmergencyIcon sx={{ fontSize: 40 }} />,
      color: '#d32f2f',
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {statCards.map((card) => (
          <Grid item xs={12} sm={6} md={3} key={card.title}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative',
                overflow: 'visible',
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    position: 'absolute',
                    top: -20,
                    right: 20,
                    backgroundColor: card.color,
                    borderRadius: '50%',
                    width: 60,
                    height: 60,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                  }}
                >
                  {card.icon}
                </Box>
                
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  {card.title}
                </Typography>
                
                <Typography variant="h3" component="div">
                  {card.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {/* Add more dashboard sections here */}
    </Box>
  );
};

export default Dashboard; 