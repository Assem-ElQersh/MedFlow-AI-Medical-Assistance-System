import os
import json
from pneumonia_classifier import main as train_model
import torch

def test_configurations():
    """Test different model configurations"""
    
    # Define configurations to test
    configs = [
        {
            'name': 'resnet50_default',
            'model_type': 'resnet50',
            'batch_size': 32,
            'learning_rate': 0.001,
            'num_epochs': 50
        },
        {
            'name': 'densenet121_default',
            'model_type': 'densenet121',
            'batch_size': 32,
            'learning_rate': 0.001,
            'num_epochs': 50
        },
        {
            'name': 'efficientnet_b0_default',
            'model_type': 'efficientnet_b0',
            'batch_size': 32,
            'learning_rate': 0.001,
            'num_epochs': 50
        },
        {
            'name': 'resnet50_large_batch',
            'model_type': 'resnet50',
            'batch_size': 64,
            'learning_rate': 0.001,
            'num_epochs': 50
        },
        {
            'name': 'resnet50_high_lr',
            'model_type': 'resnet50',
            'batch_size': 32,
            'learning_rate': 0.01,
            'num_epochs': 50
        }
    ]
    
    # Create results directory
    results_dir = 'ml_models/disease_classifiers/pneumonia/results/config_tests'
    os.makedirs(results_dir, exist_ok=True)
    
    # Test each configuration
    for config in configs:
        print(f"\nTesting configuration: {config['name']}")
        
        # Update configuration
        from pneumonia_classifier import CONFIG
        CONFIG.update({
            'data_dir': 'ml_models/data_preparation/datasets/pneumonia',
            'model_type': config['model_type'],
            'batch_size': config['batch_size'],
            'learning_rate': config['learning_rate'],
            'num_epochs': config['num_epochs'],
            'results_dir': os.path.join(results_dir, config['name'])
        })
        
        # Create configuration-specific directories
        os.makedirs(CONFIG['results_dir'], exist_ok=True)
        os.makedirs(os.path.join(CONFIG['model_save_dir'], config['name']), exist_ok=True)
        
        # Save configuration
        with open(os.path.join(CONFIG['results_dir'], 'config.json'), 'w') as f:
            json.dump(config, f, indent=4)
        
        try:
            # Train model with current configuration
            train_model()
            
            # Save GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
        except Exception as e:
            print(f"Error in configuration {config['name']}: {str(e)}")
            continue

if __name__ == '__main__':
    test_configurations() 