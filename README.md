# MedFlow: AI Medical Assistance System

MedFlow is an advanced, modular AI-powered medical assistance system for automated diagnosis, medical image analysis, and expert recommendations.  
It is designed for extensibility, clinical research, and real-world deployment.

---

## Features

- **AI Disease Detection**: Pneumonia (implemented), Tuberculosis, COVID-19, Brain Tumor, Skin Cancer (planned)
- **Medical Image Enhancement**: Super-Resolution (SISR) for improved diagnostic quality
- **Expert System**: Rule-based symptom analysis, risk assessment, and treatment recommendations
- **Backend API**: FastAPI-based, secure, and ready for integration
- **Data Preparation**: Unified dataset downloader and preprocessing pipelines
- **Extensible Architecture**: Easily add new diseases, models, and expert rules
- **(Planned) Frontend**: User-friendly web interface for clinicians and patients

---

## Project Structure

```
MedFlow/
├── backend/
│   └── app/
│       ├── api/         # API endpoints (diagnosis, history, etc.)
│       ├── core/        # Core backend logic
│       ├── db/          # Database models and migrations
│       ├── models/      # Pydantic models
│       ├── schemas/     # API schemas
│       ├── services/    # AI service integration
│       └── main.py      # FastAPI entrypoint
├── ml_models/
│   ├── disease_classifiers/
│   │   └── pneumonia/
│   │       ├── training/
│   │       ├── models/
│   │       └── results/
│   ├── data_preparation/
│   │   ├── unified_downloader.py
│   │   ├── preprocess_datasets.py
│   │   └── datasets/   # (excluded from git)
│   ├── image_enhancement/
│   │   └── training/sisr_model.py
│   └── expert_system/
│       ├── rules_engine/inference.py
│       └── knowledge_base/rules.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- (Recommended) CUDA-capable GPU for model training/inference
- PostgreSQL (for backend)
- Node.js & npm (for planned frontend)

### 1. Environment Setup

**Using Conda:**
```bash
conda create -n medflow python=3.8
conda activate medflow
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install -r requirements.txt
```

**Or using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download Datasets

> **Note:** Datasets are NOT included in the repo.  
> They are automatically excluded by `.gitignore`.

Run the unified downloader:
```bash
python ml_models/data_preparation/unified_downloader.py
```
This will download all required datasets to `ml_models/data_preparation/datasets/`.

### 3. Preprocess Datasets

```bash
python ml_models/data_preparation/preprocess_datasets.py
```
This will clean, crop, and split all datasets for model training.

### 4. Train Models

- Pneumonia (example):
  ```bash
  python ml_models/disease_classifiers/pneumonia/training/test_configurations.py
  ```
- (Planned) Add and run training scripts for TB, COVID-19, brain tumor, and skin cancer.

### 5. Run the Backend

```bash
cd backend
uvicorn app.main:app --reload
```
API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Usage

- **Diagnosis API**: Submit symptoms, vital signs, and/or images for automated diagnosis and recommendations.
- **Image Enhancement**: Super-resolve medical images for better analysis.
- **Expert System**: Get rule-based analysis and emergency alerts.

---

## Development Roadmap

### Implemented

- Pneumonia classifier (ResNet, DenseNet, EfficientNet)
- SISR image enhancement
- Unified dataset downloader & preprocessing
- Expert system (symptom analysis, risk, treatment)
- Modular backend API

### In Progress / Planned

- Add classifiers for: Tuberculosis, COVID-19, Brain Tumor, Skin Cancer
- Expand expert system knowledge base
- Frontend web interface (React or similar)
- Telemedicine and real-time alert integration
- More robust testing and CI/CD
- Dockerization and deployment scripts

---

## Contributing

1. Fork the repo and create a feature branch
2. Commit your changes
3. Push and open a Pull Request
4. Please follow code style and add tests where possible

---

## License

MIT License. See `LICENSE` for details.

---

## Contact

- [Assem ElQersh](https://github.com/Assem-ElQersh)
- Issues and feature requests: [GitHub Issues](https://github.com/Assem-ElQersh/MedFlow-AI-Medical-Assistance-System/issues)

---

**This README is always kept up-to-date with the latest project structure and features.** 