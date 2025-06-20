import os
import cv2
import numpy as np
from PIL import Image
import imutils
from tqdm import tqdm
import shutil
from pathlib import Path
import sys
sys.path.append('C:/Users/assem/Desktop/MedFlow-AI-Medical-Assistance-System')
from data.unified_downloader import download_all_datasets

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
        
        if dataset_type == 'pneumonia':
            # For pneumonia, use existing train/val/test split
            for split in ['train', 'val', 'test']:
                split_path = os.path.join(self.input_path, 'chest_xray', split)
                if not os.path.exists(split_path):
                    continue
                    
                # Process each class in the split
                for class_name in os.listdir(split_path):
                    class_path = os.path.join(split_path, class_name)
                    if not os.path.isdir(class_path):
                        continue
                    
                    # Create output directory
                    output_dir = os.path.join(self.output_path, dataset_type, split, class_name)
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Process all images in the class
                    image_files = [f for f in os.listdir(class_path) 
                                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    
                    for file in tqdm(image_files, desc=f"Processing {split} {class_name}"):
                        img_path = os.path.join(class_path, file)
                        processed_img = self.process_image(img_path, dataset_type)
                        
                        if processed_img is not None:
                            output_path = os.path.join(output_dir, file)
                            cv2.imwrite(output_path, cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR))
        
        elif dataset_type == 'tuberculosis':
            # Special handling for tuberculosis dataset
            db_path = os.path.join(self.input_path, 'TB_Chest_Radiography_Database')
            if not os.path.exists(db_path):
                print(f"Tuberculosis database not found at {db_path}")
                return
                
            # Create train/val/test directories
            for split in ['train', 'val', 'test']:
                os.makedirs(os.path.join(self.output_path, dataset_type, split), exist_ok=True)
            
            # Process Normal and Tuberculosis classes
            for class_name in ['Normal', 'Tuberculosis']:
                class_path = os.path.join(db_path, class_name)
                if not os.path.exists(class_path):
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
        
        elif dataset_type == 'covid':
            # Special handling for COVID-19 dataset
            db_path = os.path.join(self.input_path, 'COVID-19_Radiography_Dataset')
            if not os.path.exists(db_path):
                print(f"COVID-19 database not found at {db_path}")
                return
                
            # Create train/val/test directories
            for split in ['train', 'val', 'test']:
                os.makedirs(os.path.join(self.output_path, dataset_type, split), exist_ok=True)
            
            # Process all classes
            for class_name in ['COVID', 'Normal', 'Lung_Opacity', 'Viral Pneumonia']:
                class_path = os.path.join(db_path, class_name, 'images')
                if not os.path.exists(class_path):
                    print(f"Class path not found: {class_path}")
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
        
        elif dataset_type == 'brain_tumor':
            # Special handling for brain tumor dataset
            # Create train/val/test directories
            for split in ['train', 'val', 'test']:
                os.makedirs(os.path.join(self.output_path, dataset_type, split), exist_ok=True)
            
            # Process Training data (70% train, 15% val, 15% test)
            training_path = os.path.join(self.input_path, 'Training')
            if os.path.exists(training_path):
                for class_name in ['glioma', 'meningioma', 'notumor', 'pituitary']:
                    class_path = os.path.join(training_path, class_name)
                    if not os.path.exists(class_path):
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
            
            # Process Testing data (all goes to test set)
            testing_path = os.path.join(self.input_path, 'Testing')
            if os.path.exists(testing_path):
                for class_name in ['glioma', 'meningioma', 'notumor', 'pituitary']:
                    class_path = os.path.join(testing_path, class_name)
                    if not os.path.exists(class_path):
                        continue
                    
                    # Get all images
                    image_files = [f for f in os.listdir(class_path) 
                                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    
                    # Process all images
                    output_dir = os.path.join(self.output_path, dataset_type, 'test', class_name)
                    os.makedirs(output_dir, exist_ok=True)
                    
                    for file in tqdm(image_files, desc=f"Processing test {class_name}"):
                        img_path = os.path.join(class_path, file)
                        processed_img = self.process_image(img_path, dataset_type)
                        
                        if processed_img is not None:
                            output_path = os.path.join(output_dir, file)
                            cv2.imwrite(output_path, cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR))
        
        else:
            # Original preprocessing logic for other datasets (skin cancer)
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
        'pneumonia': {
            'input': 'data/pneumonia',
            'output': 'data/pneumonia/processed'
        },
        'tuberculosis': {
            'input': 'data/tuberculosis',
            'output': 'data/tuberculosis/processed'
        },
        'covid': {
            'input': 'data/covid19',
            'output': 'data/covid19/processed'
        },
        'brain_tumor': {
            'input': 'data/brain_tumor',
            'output': 'data/brain_tumor/processed'
        },
        'skin_cancer': {
            'input': 'data/skin_cancer',
            'output': 'data/skin_cancer/processed'
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