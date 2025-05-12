import os
import sys
import kagglehub
import shutil
from pathlib import Path
from tqdm import tqdm
import logging

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_models/data_preparation/download.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def ensure_dir(directory):
    """Create directory if it doesn't exist"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def download_dataset(dataset_id, dest_path, dataset_name):
    """Download a single dataset with error handling"""
    try:
        logging.info(f"Downloading {dataset_name} dataset...")
        # Download to a temporary directory first
        temp_path = kagglehub.dataset_download(dataset_id)
        
        # Move the downloaded files to the desired location
        if os.path.exists(temp_path):
            ensure_dir(dest_path)
            for item in os.listdir(temp_path):
                src = os.path.join(temp_path, item)
                dst = os.path.join(dest_path, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            # Clean up temporary directory
            shutil.rmtree(temp_path)
            logging.info(f"{dataset_name} dataset downloaded to: {dest_path}")
            return dest_path
        else:
            raise Exception(f"Downloaded files not found at {temp_path}")
    except Exception as e:
        logging.error(f"Error downloading {dataset_name} dataset: {e}")
        return None

def download_all_datasets():
    """Download all required datasets"""
    # Define all datasets and their paths
    datasets = {
        "pneumonia": {
            "id": "paultimothymooney/chest-xray-pneumonia",
            "path": os.path.join("ml_models", "disease_classifiers", "pneumonia", "data")
        },
        "tuberculosis": {
            "id": "tawsifurrahman/tuberculosis-tb-chest-xray-dataset",
            "path": os.path.join("ml_models", "data_preparation", "datasets", "tuberculosis")
        },
        "covid19": {
            "id": "tawsifurrahman/covid19-radiography-database",
            "path": os.path.join("ml_models", "data_preparation", "datasets", "covid19")
        },
        "brain_tumor": {
            "id": "masoudnickparvar/brain-tumor-mri-dataset",
            "path": os.path.join("ml_models", "data_preparation", "datasets", "brain_tumor")
        },
        "skin_cancer": {
            "id": "kmader/skin-cancer-mnist-ham10000",
            "path": os.path.join("ml_models", "data_preparation", "datasets", "skin_cancer")
        }
    }
    
    results = {}
    
    # Download each dataset
    for name, info in datasets.items():
        ensure_dir(info["path"])
        results[name] = download_dataset(info["id"], info["path"], name)
    
    return results

def main():
    """Main function to download all datasets"""
    logging.info("Starting unified dataset downloader...")
    
    # Download all datasets
    results = download_all_datasets()
    
    # Print summary
    logging.info("\n===== Download Summary =====")
    for name, path in results.items():
        status = '[SUCCESS]' if path else '[FAILED]'
        logging.info(f"{name.replace('_', ' ').title()} dataset: {status}")
    
    logging.info("\nAll downloads completed. Check download.log for detailed information.")

if __name__ == "__main__":
    main() 