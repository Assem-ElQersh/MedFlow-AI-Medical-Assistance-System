import os
import requests
from pathlib import Path
import json

# API configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_IMAGES_DIR = Path(__file__).parent.parent.parent / "ml_models/disease_classifiers/pneumonia/data/chest_xray/test"

def test_file_upload():
    """Test the API with file upload"""
    print("\nTesting file upload endpoint...")
    
    # Test both normal and pneumonia cases
    for class_name in ['NORMAL', 'PNEUMONIA']:
        class_dir = TEST_IMAGES_DIR / class_name
        if not class_dir.exists():
            print(f"Warning: {class_dir} not found")
            continue
            
        # Get first image from each class
        image_files = list(class_dir.glob("*.jpeg"))[:1]
        if not image_files:
            print(f"Warning: No images found in {class_dir}")
            continue
            
        image_path = image_files[0]
        print(f"\nTesting with {class_name} image: {image_path.name}")
        
        # Test with file upload
        url = f"{BASE_URL}/pneumonia/diagnose"
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Probabilities: {json.dumps(result['probabilities'], indent=2)}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

def test_file_path():
    """Test the API with file path"""
    print("\nTesting file path endpoint...")
    
    # Test both normal and pneumonia cases
    for class_name in ['NORMAL', 'PNEUMONIA']:
        class_dir = TEST_IMAGES_DIR / class_name
        if not class_dir.exists():
            print(f"Warning: {class_dir} not found")
            continue
            
        # Get first image from each class
        image_files = list(class_dir.glob("*.jpeg"))[:1]
        if not image_files:
            print(f"Warning: No images found in {class_dir}")
            continue
            
        image_path = image_files[0]
        print(f"\nTesting with {class_name} image: {image_path.name}")
        
        # Test with file path
        url = f"{BASE_URL}/pneumonia/diagnose"
        data = {
            "image_path": str(image_path),
            "model_type": "resnet50"
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Probabilities: {json.dumps(result['probabilities'], indent=2)}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

def test_different_models():
    """Test the API with different model types"""
    print("\nTesting different model types...")
    
    # Get a test image
    test_image = next(TEST_IMAGES_DIR.glob("**/*.jpeg"))
    print(f"\nTesting with image: {test_image.name}")
    
    # Test each model type
    for model_type in ['resnet50', 'densenet121', 'efficientnet_b0']:
        print(f"\nModel: {model_type}")
        
        url = f"{BASE_URL}/pneumonia/diagnose"
        data = {
            "image_path": str(test_image),
            "model_type": model_type
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Prediction: {result['prediction']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Probabilities: {json.dumps(result['probabilities'], indent=2)}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    print("Starting Pneumonia API Tests...")
    
    # Run tests
    test_file_upload()
    test_file_path()
    test_different_models()
    
    print("\nTests completed!") 