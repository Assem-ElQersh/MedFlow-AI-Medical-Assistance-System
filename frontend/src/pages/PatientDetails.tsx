import {
    ArrowBack as ArrowBackIcon,
    Edit as EditIcon,
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    CircularProgress,
    Divider,
    Grid,
    Paper,
    Tab,
    Tabs,
    Typography,
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { apiService } from '../services/api';

interface Patient {
  id: string;
  fullName: string;
  email: string;
  dateOfBirth: string;
  gender: string;
  phone: string;
  address: string;
  medicalHistory: MedicalRecord[];
  emergencyContacts: EmergencyContact[];
}

interface MedicalRecord {
  id: string;
  date: string;
  diagnosis: string;
  treatment: string;
  doctor: string;
  notes: string;
}

interface EmergencyContact {
  name: string;
  relationship: string;
  phone: string;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`patient-tabpanel-${index}`}
      aria-labelledby={`patient-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const PatientDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    fetchPatientDetails();
  }, [id]);

  const fetchPatientDetails = async () => {
    try {
      setLoading(true);
      const response = await apiService.getPatient(id!);
      setPatient(response);
    } catch (err: any) {
      setError(err.message || 'Failed to load patient details');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    );
  }

  if (!patient) {
    return (
      <Alert severity="warning">
        Patient not found
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/patients')}
        >
          Back to Patients
        </Button>
        <Button
          variant="contained"
          startIcon={<EditIcon />}
          onClick={() => navigate(`/patients/${id}/edit`)}
        >
          Edit Patient
        </Button>
      </Box>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          {patient.fullName}
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" color="textSecondary">
              Personal Information
            </Typography>
            <Box mt={2}>
              <Typography><strong>Email:</strong> {patient.email}</Typography>
              <Typography><strong>Date of Birth:</strong> {patient.dateOfBirth}</Typography>
              <Typography><strong>Gender:</strong> {patient.gender}</Typography>
              <Typography><strong>Phone:</strong> {patient.phone}</Typography>
              <Typography><strong>Address:</strong> {patient.address}</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" color="textSecondary">
              Emergency Contacts
            </Typography>
            <Box mt={2}>
              {patient.emergencyContacts.map((contact, index) => (
                <Box key={index} mb={2}>
                  <Typography><strong>{contact.name}</strong> ({contact.relationship})</Typography>
                  <Typography>{contact.phone}</Typography>
                </Box>
              ))}
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ width: '100%' }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          aria-label="patient tabs"
        >
          <Tab label="Medical History" />
          <Tab label="Diagnoses" />
          <Tab label="Prescriptions" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          {patient.medicalHistory.map((record) => (
            <Box key={record.id} mb={3}>
              <Typography variant="h6">
                {record.date} - {record.diagnosis}
              </Typography>
              <Typography color="textSecondary">
                Doctor: {record.doctor}
              </Typography>
              <Typography paragraph>
                Treatment: {record.treatment}
              </Typography>
              <Typography>
                Notes: {record.notes}
              </Typography>
              <Divider sx={{ my: 2 }} />
            </Box>
          ))}
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          {/* Diagnoses tab content */}
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          {/* Prescriptions tab content */}
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default PatientDetails; 