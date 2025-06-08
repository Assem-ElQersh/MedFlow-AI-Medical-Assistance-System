import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    CardMedia,
    Chip,
    CircularProgress,
    Grid,
    Paper,
    Typography,
} from '@mui/material';
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { apiService } from '../services/api';

interface ImageAnalysis {
  id: string;
  imageUrl: string;
  modality: string;
  findings: string[];
  confidence: number;
  recommendations: string[];
  timestamp: string;
}

const Radiology: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<ImageAnalysis | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    const formData = new FormData();
    formData.append('image', file);

    try {
      setLoading(true);
      setError(null);
      const result = await apiService.analyzeImage(formData);
      setAnalysis(result);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.dicom'],
    },
    maxFiles: 1,
  });

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Radiology Image Analysis
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper
            {...getRootProps()}
            sx={{
              p: 3,
              textAlign: 'center',
              cursor: 'pointer',
              backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'divider',
            }}
          >
            <input {...getInputProps()} />
            {loading ? (
              <CircularProgress />
            ) : (
              <Box>
                <Typography variant="h6" gutterBottom>
                  {isDragActive
                    ? 'Drop the image here'
                    : 'Drag and drop an image here, or click to select'}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Supported formats: JPEG, PNG, DICOM
                </Typography>
                <Button variant="contained" sx={{ mt: 2 }}>
                  Select Image
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          {analysis && (
            <Card>
              <CardMedia
                component="img"
                height="300"
                image={analysis.imageUrl}
                alt="Radiology image"
              />
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <Typography variant="h6" sx={{ mr: 2 }}>
                    Analysis Results
                  </Typography>
                  <Chip
                    label={`${Math.round(analysis.confidence * 100)}% Confidence`}
                    color={analysis.confidence > 0.8 ? 'success' : 'warning'}
                  />
                </Box>

                <Typography variant="subtitle1" gutterBottom>
                  Modality: {analysis.modality}
                </Typography>

                <Typography variant="subtitle1" gutterBottom>
                  Findings:
                </Typography>
                <Box component="ul" sx={{ pl: 2 }}>
                  {analysis.findings.map((finding, index) => (
                    <Typography component="li" key={index}>
                      {finding}
                    </Typography>
                  ))}
                </Box>

                <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
                  Recommendations:
                </Typography>
                <Box component="ul" sx={{ pl: 2 }}>
                  {analysis.recommendations.map((recommendation, index) => (
                    <Typography component="li" key={index}>
                      {recommendation}
                    </Typography>
                  ))}
                </Box>

                <Typography
                  variant="caption"
                  color="textSecondary"
                  sx={{ display: 'block', mt: 2 }}
                >
                  Analyzed on: {new Date(analysis.timestamp).toLocaleString()}
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default Radiology; 