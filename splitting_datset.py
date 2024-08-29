import os
import shutil

# Define the path to the directory containing the images
source_dir = "dataset/indoor/NH-HAZE"
gt_dir = "dataset/indoor/NH-HAZE/GT"
hazy_dir = "dataset/indoor/NH-HAZE/hazy"

# Create directories if they don't exist
os.makedirs(gt_dir, exist_ok=True)
os.makedirs(hazy_dir, exist_ok=True)

# Loop through all the files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Add other file types if necessary
        if "GT" in filename:  # Adjust this condition to match your GT images naming convention
            shutil.move(os.path.join(source_dir, filename), os.path.join(gt_dir, filename))
        elif "hazy" in filename:  # Adjust this condition to match your hazy images naming convention
            shutil.move(os.path.join(source_dir, filename), os.path.join(hazy_dir, filename))

print("Images have been successfully divided into GT and hazy folders.")
