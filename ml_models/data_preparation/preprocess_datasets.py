import os
import cv2
import numpy as np
from PIL import Image
import imutils
from tqdm import tqdm
import shutil
from pathlib import Path

class DatasetPreprocessor:
    def __init__(self, input_path, output_path, target_size=(224, 224)):
        self.input_path = input_path
        self.output_path = output_path
        self.target_size = target_size
        os.makedirs(output_path, exist_ok=True)
    
    def crop_brain_tumor(self, img):
        """Crop brain tumor MRI images to remove extra margins"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        
        ADD_PIXELS = 0
        new_img = img[extTop[1]-ADD_PIXELS:extBot[1]+ADD_PIXELS, 
                     extLeft[0]-ADD_PIXELS:extRight[0]+ADD_PIXELS].copy()
        return new_img
    
    def preprocess_xray(self, img):
        """Preprocess X-ray images (Pneumonia, TB, COVID)"""
        # Convert to grayscale
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Normalize
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        
        # Apply CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img = clahe.apply(img)
        
        # Convert back to RGB
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        return img
    
    def preprocess_skin(self, img):
        """Preprocess skin cancer images"""
        # Convert to RGB if needed
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        
        # Normalize
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        
        # Apply slight Gaussian blur to reduce noise
        img = cv2.GaussianBlur(img, (3, 3), 0)
        return img
    
    def process_image(self, img_path, dataset_type):
        """Process image based on dataset type"""
        try:
            img = cv2.imread(img_path)
            if img is None:
                return None
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Apply dataset-specific preprocessing
            if dataset_type == 'brain_tumor':
                img = self.crop_brain_tumor(img)
            elif dataset_type in ['pneumonia', 'tuberculosis', 'covid']:
                img = self.preprocess_xray(img)
            elif dataset_type == 'skin_cancer':
                img = self.preprocess_skin(img)
            
            # Resize to target size
            img = cv2.resize(img, self.target_size)
            return img
            
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            return None
    
    def preprocess_dataset(self, dataset_type):
        """Preprocess entire dataset"""
        print(f"\nPreprocessing {dataset_type} dataset...")
        
        # Create train/val/test directories
        for split in ['train', 'val', 'test']:
            os.makedirs(os.path.join(self.output_path, dataset_type, split), exist_ok=True)
        
        # Process each class
        for class_name in os.listdir(self.input_path):
            class_path = os.path.join(self.input_path, class_name)
            if not os.path.isdir(class_path):
                continue
            
            # Get all images
            image_files = [f for f in os.listdir(class_path) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Shuffle and split
            np.random.shuffle(image_files)
            n = len(image_files)
            train_files = image_files[:int(0.7*n)]
            val_files = image_files[int(0.7*n):int(0.85*n)]
            test_files = image_files[int(0.85*n):]
            
            # Process each split
            for split, files in [('train', train_files), 
                               ('val', val_files), 
                               ('test', test_files)]:
                output_dir = os.path.join(self.output_path, dataset_type, split, class_name)
                os.makedirs(output_dir, exist_ok=True)
                
                for file in tqdm(files, desc=f"Processing {split} {class_name}"):
                    img_path = os.path.join(class_path, file)
                    processed_img = self.process_image(img_path, dataset_type)
                    
                    if processed_img is not None:
                        output_path = os.path.join(output_dir, file)
                        cv2.imwrite(output_path, cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR))

def main():
    # Define dataset paths
    datasets = {
        'tuberculosis': {
            'input': 'ml_models/data_preparation/datasets/tuberculosis',
            'output': 'ml_models/data_preparation/processed/tuberculosis'
        },
        'covid': {
            'input': 'ml_models/data_preparation/datasets/covid19',
            'output': 'ml_models/data_preparation/processed/covid'
        },
        'brain_tumor': {
            'input': 'ml_models/data_preparation/datasets/brain_tumor',
            'output': 'ml_models/data_preparation/processed/brain_tumor'
        },
        'skin_cancer': {
            'input': 'ml_models/data_preparation/datasets/skin_cancer',
            'output': 'ml_models/data_preparation/processed/skin_cancer'
        }
    }
    
    # Process each dataset
    for dataset_type, paths in datasets.items():
        preprocessor = DatasetPreprocessor(
            input_path=paths['input'],
            output_path=paths['output']
        )
        preprocessor.preprocess_dataset(dataset_type)

if __name__ == "__main__":
    main() 