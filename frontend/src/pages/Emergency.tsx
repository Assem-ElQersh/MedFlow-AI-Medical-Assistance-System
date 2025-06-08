import {
    CheckCircle as CheckCircleIcon,
    LocalHospital as HospitalIcon,
    Phone as PhoneIcon,
    AccessTime as TimeIcon,
    Warning as WarningIcon,
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Grid,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Paper,
    Typography,
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

interface EmergencyCase {
  id: string;
  patientId: string;
  patientName: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  symptoms: string[];
  vitalSigns: {
    heartRate: number;
    bloodPressure: string;
    temperature: number;
    oxygenSaturation: number;
  };
  status: 'active' | 'resolved' | 'in_progress';
  timestamp: string;
  assignedTo?: string;
}

const Emergency: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [emergencies, setEmergencies] = useState<EmergencyCase[]>([]);

  useEffect(() => {
    fetchEmergencies();
    const interval = setInterval(fetchEmergencies, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchEmergencies = async () => {
    try {
      setLoading(true);
      const response = await apiService.getEmergencies();
      setEmergencies(response);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch emergency cases');
    } finally {
      setLoading(false);
    }
  };

  const handleAssignCase = async (caseId: string) => {
    try {
      await apiService.assignEmergencyCase(caseId);
      fetchEmergencies();
    } catch (err: any) {
      setError(err.message || 'Failed to assign case');
    }
  };

  const handleResolveCase = async (caseId: string) => {
    try {
      await apiService.resolveEmergencyCase(caseId);
      fetchEmergencies();
    } catch (err: any) {
      setError(err.message || 'Failed to resolve case');
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      default:
        return 'success';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <WarningIcon color="error" />;
      case 'in_progress':
        return <TimeIcon color="warning" />;
      case 'resolved':
        return <CheckCircleIcon color="success" />;
      default:
        return null;
    }
  };

  if (loading && emergencies.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Emergency Response
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {emergencies.map((emergency) => (
          <Grid item xs={12} md={6} key={emergency.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6">
                    {emergency.patientName}
                  </Typography>
                  <Chip
                    label={emergency.urgency.toUpperCase()}
                    color={getUrgencyColor(emergency.urgency)}
                  />
                </Box>

                <List dense>
                  <ListItem>
                    <ListItemIcon>
                      <HospitalIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Vital Signs"
                      secondary={
                        <>
                          Heart Rate: {emergency.vitalSigns.heartRate} bpm
                          <br />
                          BP: {emergency.vitalSigns.bloodPressure}
                          <br />
                          Temp: {emergency.vitalSigns.temperature}°C
                          <br />
                          O2: {emergency.vitalSigns.oxygenSaturation}%
                        </>
                      }
                    />
                  </ListItem>

                  <ListItem>
                    <ListItemIcon>
                      <WarningIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Symptoms"
                      secondary={emergency.symptoms.join(', ')}
                    />
                  </ListItem>

                  <ListItem>
                    <ListItemIcon>
                      <TimeIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Reported"
                      secondary={new Date(emergency.timestamp).toLocaleString()}
                    />
                  </ListItem>

                  {emergency.assignedTo && (
                    <ListItem>
                      <ListItemIcon>
                        <PhoneIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="Assigned To"
                        secondary={emergency.assignedTo}
                      />
                    </ListItem>
                  )}
                </List>

                <Box display="flex" justifyContent="flex-end" mt={2}>
                  {emergency.status === 'active' && (
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => handleAssignCase(emergency.id)}
                      sx={{ mr: 1 }}
                    >
                      Assign Case
                    </Button>
                  )}
                  {emergency.status === 'in_progress' && (
                    <Button
                      variant="contained"
                      color="success"
                      onClick={() => handleResolveCase(emergency.id)}
                    >
                      Resolve Case
                    </Button>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}

        {emergencies.length === 0 && !loading && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="h6" color="textSecondary">
                No active emergency cases
              </Typography>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default Emergency; 