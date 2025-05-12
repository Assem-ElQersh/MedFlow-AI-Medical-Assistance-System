# MedFlow: AI Medical Assistance System

A comprehensive medical imaging analysis platform that combines deep learning models with expert systems for accurate disease diagnosis and image enhancement.

## Features

### 1. Disease Classification
- **Pneumonia Detection** (✅ Implemented)
  - Uses ResNet50 model for chest X-ray analysis
  - Supports both normal and pneumonia cases
  - Provides confidence scores and class probabilities
  - API endpoint available for integration

- **Other Disease Classifiers** (🚧 In Progress)
  - Tuberculosis Detection
  - COVID-19 Detection
  - Brain Tumor Detection
  - Skin Cancer Detection

### 2. Image Enhancement
- **Super-Resolution** (🚧 In Progress)
  - Enhanced image quality
  - Improved diagnostic accuracy

### 3. Expert System
- **Rule-based Diagnosis** (🚧 In Progress)
  - Combines AI predictions with medical knowledge
  - Provides comprehensive diagnostic reports

## Project Structure

```
MedFlow/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   └── tests/              # API tests
├── ml_models/              # Machine learning models
│   ├── disease_classifiers/
│   │   └── pneumonia/      # Pneumonia classifier
│   ├── image_enhancement/  # SISR model
│   └── expert_system/      # Rule-based system
└── frontend/               # React frontend (coming soon)
```

## API Documentation

### Pneumonia Detection API

#### Endpoint: `/api/v1/pneumonia/diagnose`

**Method:** POST

**Input Options:**
1. File Upload:
   ```python
   import requests
   
   url = "http://localhost:8000/api/v1/pneumonia/diagnose"
   files = {"file": open("chest_xray.jpg", "rb")}
   response = requests.post(url, files=files)
   print(response.json())
   ```

2. File Path (if file is on server):
   ```python
   import requests
   
   url = "http://localhost:8000/api/v1/pneumonia/diagnose"
   data = {
       "image_path": "/path/to/chest_xray.jpg"
   }
   response = requests.post(url, json=data)
   print(response.json())
   ```

**Response Format:**
```json
{
    "prediction": "NORMAL",  // or "PNEUMONIA"
    "confidence": 0.889,     // confidence score
    "probabilities": {
        "NORMAL": 0.889,
        "PNEUMONIA": 0.111
    }
}
```

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/MedFlow.git
   cd MedFlow
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run tests:**
   ```bash
   python tests/test_pneumonia_api.py
   ```

## Next Steps

1. **Backend Development**
   - [ ] Implement remaining disease classifiers
   - [ ] Add image enhancement endpoints
   - [ ] Integrate expert system
   - [ ] Add user authentication
   - [ ] Add database integration

2. **Frontend Development**
   - [ ] Create React application
   - [ ] Implement user interface
   - [ ] Add real-time predictions
   - [ ] Create visualization components

3. **Model Improvements**
   - [ ] Train and integrate additional disease classifiers
   - [ ] Optimize model performance
   - [ ] Add model versioning
   - [ ] Implement model monitoring

4. **Documentation**
   - [ ] Add API documentation
   - [ ] Create user guides
   - [ ] Add deployment instructions
   - [ ] Document model training process

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

- [Assem ElQersh](https://github.com/Assem-ElQersh)
- Issues and feature requests: [GitHub Issues](https://github.com/Assem-ElQersh/MedFlow-AI-Medical-Assistance-System/issues)

---

**This README is always kept up-to-date with the latest project structure and features.** 