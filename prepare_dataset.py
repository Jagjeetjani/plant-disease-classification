import os
import json
import numpy as np
from PIL import Image
import cv2
from create_leaf_samples import generate_realistic_leaf_image, DISEASE_DB

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")

SPLITS = {
    "train": 50,
    "val": 15,
    "test": 15
}

def create_dataset():
    print(f"Creating PlantVillage dataset structure in: {DATASET_DIR}")
    total_created = 0
    
    for split, count in SPLITS.items():
        split_dir = os.path.join(DATASET_DIR, split)
        os.makedirs(split_dir, exist_ok=True)
        
        for class_idx, class_key in enumerate(DISEASE_DB.keys()):
            class_folder = os.path.join(split_dir, class_key)
            os.makedirs(class_folder, exist_ok=True)
            
            for i in range(count):
                seed = (class_idx * 1000) + (100 if split == "train" else 500 if split == "val" else 900) + i
                img = generate_realistic_leaf_image(class_key, size=(128, 128), seed=seed)
                img_path = os.path.join(class_folder, f"leaf_{split}_{i:03d}.jpg")
                Image.fromarray(img).save(img_path, quality=90)
                total_created += 1
                
        print(f"Finished split: {split} ({count * len(DISEASE_DB)} images across {len(DISEASE_DB)} classes)")

    print(f"Total images created: {total_created} across train/val/test splits.")

if __name__ == "__main__":
    create_dataset()
