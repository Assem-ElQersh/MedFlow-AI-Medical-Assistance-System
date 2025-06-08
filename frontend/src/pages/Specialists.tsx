import {
    Alert,
    Avatar,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControl,
    Grid,
    InputLabel,
    MenuItem,
    Rating,
    Select,
    TextField,
    Typography
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';

interface Specialist {
  id: string;
  name: string;
  specialty: string;
  subSpecialties: string[];
  experience: number;
  rating: number;
  availability: {
    nextAvailable: string;
    schedule: {
      day: string;
      slots: string[];
    }[];
  };
  location: string;
  contact: string;
}

interface AppointmentRequest {
  specialistId: string;
  patientId: string;
  date: string;
  time: string;
  reason: string;
  urgency: 'routine' | 'urgent' | 'emergency';
}

const Specialists: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [specialists, setSpecialists] = useState<Specialist[]>([]);
  const [selectedSpecialist, setSelectedSpecialist] = useState<Specialist | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [appointmentRequest, setAppointmentRequest] = useState<AppointmentRequest>({
    specialistId: '',
    patientId: '',
    date: '',
    time: '',
    reason: '',
    urgency: 'routine',
  });

  useEffect(() => {
    fetchSpecialists();
  }, []);

  const fetchSpecialists = async () => {
    try {
      setLoading(true);
      const response = await apiService.getSpecialists();
      setSpecialists(response);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch specialists');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (specialist: Specialist) => {
    setSelectedSpecialist(specialist);
    setAppointmentRequest({
      ...appointmentRequest,
      specialistId: specialist.id,
    });
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedSpecialist(null);
  };

  const handleAppointmentRequest = async () => {
    try {
      await apiService.requestAppointment(appointmentRequest);
      handleCloseDialog();
      // Show success message or update UI
    } catch (err: any) {
      setError(err.message || 'Failed to request appointment');
    }
  };

  if (loading && specialists.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Specialist Directory
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {specialists.map((specialist) => (
          <Grid item xs={12} md={6} key={specialist.id}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <Avatar
                    sx={{ width: 64, height: 64, mr: 2 }}
                    alt={specialist.name}
                  />
                  <Box>
                    <Typography variant="h6">
                      {specialist.name}
                    </Typography>
                    <Typography color="textSecondary">
                      {specialist.specialty}
                    </Typography>
                    <Rating value={specialist.rating} readOnly size="small" />
                  </Box>
                </Box>

                <Box mb={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Sub-specialties:
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {specialist.subSpecialties.map((subSpecialty) => (
                      <Chip
                        key={subSpecialty}
                        label={subSpecialty}
                        size="small"
                      />
                    ))}
                  </Box>
                </Box>

                <Box mb={2}>
                  <Typography variant="body2">
                    <strong>Experience:</strong> {specialist.experience} years
                  </Typography>
                  <Typography variant="body2">
                    <strong>Location:</strong> {specialist.location}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Next Available:</strong>{' '}
                    {new Date(specialist.availability.nextAvailable).toLocaleString()}
                  </Typography>
                </Box>

                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => handleOpenDialog(specialist)}
                >
                  Request Appointment
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Request Appointment</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Patient ID"
              value={appointmentRequest.patientId}
              onChange={(e) =>
                setAppointmentRequest({
                  ...appointmentRequest,
                  patientId: e.target.value,
                })
              }
              margin="normal"
            />

            <TextField
              fullWidth
              label="Date"
              type="date"
              value={appointmentRequest.date}
              onChange={(e) =>
                setAppointmentRequest({
                  ...appointmentRequest,
                  date: e.target.value,
                })
              }
              margin="normal"
              InputLabelProps={{ shrink: true }}
            />

            <FormControl fullWidth margin="normal">
              <InputLabel>Time Slot</InputLabel>
              <Select
                value={appointmentRequest.time}
                label="Time Slot"
                onChange={(e) =>
                  setAppointmentRequest({
                    ...appointmentRequest,
                    time: e.target.value,
                  })
                }
              >
                {selectedSpecialist?.availability.schedule
                  .find((day) => day.day === appointmentRequest.date)
                  ?.slots.map((slot) => (
                    <MenuItem key={slot} value={slot}>
                      {slot}
                    </MenuItem>
                  ))}
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Reason for Visit"
              multiline
              rows={4}
              value={appointmentRequest.reason}
              onChange={(e) =>
                setAppointmentRequest({
                  ...appointmentRequest,
                  reason: e.target.value,
                })
              }
              margin="normal"
            />

            <FormControl fullWidth margin="normal">
              <InputLabel>Urgency</InputLabel>
              <Select
                value={appointmentRequest.urgency}
                label="Urgency"
                onChange={(e) =>
                  setAppointmentRequest({
                    ...appointmentRequest,
                    urgency: e.target.value as 'routine' | 'urgent' | 'emergency',
                  })
                }
              >
                <MenuItem value="routine">Routine</MenuItem>
                <MenuItem value="urgent">Urgent</MenuItem>
                <MenuItem value="emergency">Emergency</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleAppointmentRequest}
            disabled={
              !appointmentRequest.patientId ||
              !appointmentRequest.date ||
              !appointmentRequest.time ||
              !appointmentRequest.reason
            }
          >
            Request Appointment
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Specialists; 