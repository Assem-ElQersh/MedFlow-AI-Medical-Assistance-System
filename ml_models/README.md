# ML Models for MedFlow AI Medical Assistance System

This directory contains the machine learning models and utilities for the MedFlow AI Medical Assistance System.

## Directory Structure

- **data_preparation/**: Contains utilities for downloading, preprocessing, and analyzing datasets.
  - `preprocess_datasets.py`: Script for preprocessing datasets.
  - `analysis/`: Contains analysis outputs (plots, statistics).
  - `datasets/`: Contains raw and processed datasets.

- **disease_classifiers/**: Contains models for disease classification.
  - **pneumonia/**: Contains the pneumonia classifier.
    - `data/`: Contains the dataset for the pneumonia classifier.
    - `training/`: Contains training scripts and utilities.
    - `results/`: Contains results and configuration tests.

- **image_enhancement/**: Contains utilities for image enhancement.
  - `training/`: Contains training scripts for image enhancement models.

- **expert_system/**: Contains the expert system for decision support.
  - `rules_engine/`: Contains the rules engine for the expert system.
  - `knowledge_base/`: Contains the knowledge base for the expert system.

## Usage

- To download datasets, run:
  ```sh
  python data/unified_downloader.py
  ```

- To preprocess datasets, run:
  ```sh
  python ml_models/data_preparation/preprocess_datasets.py
  ```

- To train the pneumonia classifier, run:
  ```sh
  python ml_models/disease_classifiers/pneumonia/training/pneumonia_classifier.py
  ```

- To train the image enhancement model, run:
  ```sh
  python ml_models/image_enhancement/training/sisr_model.py
  ```

- To use the expert system, refer to the scripts in `ml_models/expert_system/`.

## Contributing

Please ensure that all new models and utilities are added to the appropriate directory and that the README is updated accordingly. 