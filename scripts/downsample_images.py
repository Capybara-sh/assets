#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from PIL import Image

def downsample_image(input_path, output_path, scale_factor=0.25):
    """
    Downsample an image to 1/16 of its original size (1/4 width and 1/4 height).
    
    Args:
        input_path: Path to the input image
        output_path: Path where the downsampled image will be saved
        scale_factor: Scale factor for both dimensions (default 0.25 to get 1/16 area)
    """
    try:
        with Image.open(input_path) as img:
            # Calculate new dimensions (1/4 of original width and height = 1/16 area)
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            
            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save the downsampled image
            resized_img.save(output_path)
            print(f"Processed: {input_path} → {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_directory(input_dir, output_dir):
    """
    Process all images in input_dir and its subdirectories,
    maintaining the same directory structure in output_dir.
    
    Args:
        input_dir: Root directory containing images to process
        output_dir: Root directory where processed images will be saved
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    
    # Count total and processed files
    total_files = 0
    processed_files = 0
    
    # Walk through all directories and files
    for root, _, files in os.walk(input_path):
        for file in files:
            total_files += 1
            
            # Check if the file is an image
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in image_extensions:
                # Get the full path of the input file
                input_file = os.path.join(root, file)
                
                # Determine the relative path from the input directory
                rel_path = os.path.relpath(input_file, input_path)
                
                # Create the output file path with the same relative path
                output_file = os.path.join(output_path, rel_path)
                
                # Process the image
                downsample_image(input_file, output_file)
                processed_files += 1
    
    print(f"\nProcessing complete!")
    print(f"Total files found: {total_files}")
    print(f"Images processed: {processed_files}")

if __name__ == "__main__":
    # Use absolute paths with @/ alias resolution
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Source directory (imgs)
    imgs_dir = os.path.join(base_dir, "imgs")
    
    # Destination directory (img_tiny)
    img_tiny_dir = os.path.join(base_dir, "img_tiny")
    
    print(f"Downsampling images from {imgs_dir} to {img_tiny_dir}")
    process_directory(imgs_dir, img_tiny_dir) 