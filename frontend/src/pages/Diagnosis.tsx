import {
    Alert,
    Box,
    Button,
    Chip,
    CircularProgress,
    FormControl,
    Grid,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    Step,
    StepLabel,
    Stepper,
    TextField,
    Typography,
} from '@mui/material';
import React, { useState } from 'react';
import { apiService } from '../services/api';

interface Symptom {
  id: string;
  name: string;
  severity: 'mild' | 'moderate' | 'severe';
}

interface DiagnosisResult {
  possibleConditions: Array<{
    name: string;
    probability: number;
    description: string;
  }>;
  recommendations: string[];
  urgency: 'low' | 'medium' | 'high';
}

const Diagnosis: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [patientId, setPatientId] = useState('');
  const [symptoms, setSymptoms] = useState<Symptom[]>([]);
  const [selectedSymptom, setSelectedSymptom] = useState('');
  const [severity, setSeverity] = useState<'mild' | 'moderate' | 'severe'>('mild');
  const [diagnosisResult, setDiagnosisResult] = useState<DiagnosisResult | null>(null);

  const steps = ['Patient Information', 'Symptoms', 'Analysis'];

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleAddSymptom = () => {
    if (selectedSymptom) {
      setSymptoms([
        ...symptoms,
        {
          id: Date.now().toString(),
          name: selectedSymptom,
          severity,
        },
      ]);
      setSelectedSymptom('');
    }
  };

  const handleRemoveSymptom = (id: string) => {
    setSymptoms(symptoms.filter((symptom) => symptom.id !== id));
  };

  const handleAnalyze = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiService.analyzeDiagnosis({
        patientId,
        symptoms,
      });
      setDiagnosisResult(result);
      handleNext();
    } catch (err: any) {
      setError(err.message || 'Failed to analyze symptoms');
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Enter Patient Information
            </Typography>
            <TextField
              fullWidth
              label="Patient ID"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
              margin="normal"
            />
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Add Symptoms
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Symptom"
                  value={selectedSymptom}
                  onChange={(e) => setSelectedSymptom(e.target.value)}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Severity</InputLabel>
                  <Select
                    value={severity}
                    label="Severity"
                    onChange={(e) => setSeverity(e.target.value as 'mild' | 'moderate' | 'severe')}
                  >
                    <MenuItem value="mild">Mild</MenuItem>
                    <MenuItem value="moderate">Moderate</MenuItem>
                    <MenuItem value="severe">Severe</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <Button
              variant="contained"
              onClick={handleAddSymptom}
              sx={{ mt: 2 }}
            >
              Add Symptom
            </Button>

            <Box mt={3}>
              <Typography variant="subtitle1" gutterBottom>
                Selected Symptoms:
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {symptoms.map((symptom) => (
                  <Chip
                    key={symptom.id}
                    label={`${symptom.name} (${symptom.severity})`}
                    onDelete={() => handleRemoveSymptom(symptom.id)}
                    color={symptom.severity === 'severe' ? 'error' : 'default'}
                  />
                ))}
              </Box>
            </Box>
          </Box>
        );

      case 2:
        return (
          <Box>
            {loading ? (
              <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
                <CircularProgress />
              </Box>
            ) : diagnosisResult ? (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Diagnosis Results
                </Typography>
                <Alert severity={diagnosisResult.urgency === 'high' ? 'error' : 'info'} sx={{ mb: 3 }}>
                  Urgency Level: {diagnosisResult.urgency.toUpperCase()}
                </Alert>

                <Typography variant="subtitle1" gutterBottom>
                  Possible Conditions:
                </Typography>
                {diagnosisResult.possibleConditions.map((condition, index) => (
                  <Paper key={index} sx={{ p: 2, mb: 2 }}>
                    <Typography variant="h6">
                      {condition.name} ({Math.round(condition.probability * 100)}% probability)
                    </Typography>
                    <Typography color="textSecondary">
                      {condition.description}
                    </Typography>
                  </Paper>
                ))}

                <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
                  Recommendations:
                </Typography>
                <Box component="ul">
                  {diagnosisResult.recommendations.map((recommendation, index) => (
                    <Typography component="li" key={index}>
                      {recommendation}
                    </Typography>
                  ))}
                </Box>
              </Box>
            ) : null}
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        AI-Powered Diagnosis
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Stepper activeStep={activeStep}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>

      <Paper sx={{ p: 3 }}>
        {renderStepContent(activeStep)}

        <Box display="flex" justifyContent="space-between" mt={3}>
          <Button
            disabled={activeStep === 0}
            onClick={handleBack}
          >
            Back
          </Button>
          <Button
            variant="contained"
            onClick={activeStep === steps.length - 1 ? undefined : handleNext}
            disabled={
              (activeStep === 0 && !patientId) ||
              (activeStep === 1 && symptoms.length === 0) ||
              activeStep === steps.length - 1
            }
          >
            {activeStep === steps.length - 1 ? 'Finish' : 'Next'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default Diagnosis; 