# MedFlow: AI-Medical-Assistance-System

An advanced AI-powered medical assistance system that provides automated diagnosis and medical recommendations.

## Features

- AI-powered disease detection and classification
- Medical image analysis and enhancement
- Expert system for symptom analysis
- Medical chatbot for patient interaction
- Automated diagnosis and treatment recommendations
- Health monitoring and tracking
- Emergency response system

## Project Structure

```
medflow/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── alembic/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── public/
└── ml_models/
    ├── disease_classifiers/
    │   └── pneumonia/
    │       ├── data/           # Dataset storage
    │       ├── models/         # Saved model checkpoints
    │       ├── training/       # Training scripts
    │       └── results/        # Training results and metrics
    └── image_enhancement/
        └── expert_system/
```

## Setup Instructions

### Prerequisites
- Python 3.8+ or Conda environment
- PostgreSQL database
- Node.js and npm (for frontend)
- CUDA-capable GPU (recommended for AI/ML features)

### Option 1: Using Conda (Recommended for AI/ML Development)

1. Create and activate a new Conda environment:
```bash
conda create -n medflow python=3.8
conda activate medflow
```

2. Install PyTorch with CUDA support:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

3. Install additional dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Using Python Virtual Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install all dependencies:
```bash
pip install -r requirements.txt
```

### Database Setup

1. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

2. Initialize the database:
```bash
alembic upgrade head
```

### Running the Application

1. Start the backend server:
```bash
uvicorn app.main:app --reload
```

2. Start the frontend (in a new terminal):
```bash
cd frontend
npm install
npm start
```

## Testing the System

### 1. API Testing
Once the backend server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Example API Calls

#### Test Diagnosis Endpoint
```bash
curl -X POST "http://localhost:8000/api/v1/diagnosis/analyze" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": [
      {
        "name": "headache",
        "severity": 7,
        "duration": "2 days",
        "description": "Throbbing pain"
      }
    ],
    "vital_signs": {
      "blood_pressure": "120/80",
      "heart_rate": 75,
      "temperature": 37.0,
      "respiratory_rate": 16,
      "oxygen_saturation": 98.0
    }
  }'
```

### 3. Running Tests
```bash
pytest
```

## Development Notes

- The system supports both CPU and GPU (CUDA) for AI/ML operations
- AI models are loaded from the `ml_models` directory
- Database migrations are managed by Alembic
- API documentation is available through Swagger UI and ReDoc

## Troubleshooting

### Common Issues

1. **CUDA/GPU Issues**
   - Ensure CUDA is properly installed
   - Check GPU compatibility with PyTorch
   - Verify CUDA version matches PyTorch requirements

2. **Database Connection**
   - Verify PostgreSQL is running
   - Check database credentials in `.env`
   - Ensure database exists

3. **Dependencies**
   - If using Conda, ensure PyTorch is installed with CUDA support
   - For virtual environment, all dependencies are in requirements.txt

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

ml_models/disease_classifiers/pneumonia/results/config_tests/
├── resnet50_default/
├── densenet121_default/
├── efficientnet_b0_default/
├── resnet50_large_batch/
└── resnet50_high_lr/ 