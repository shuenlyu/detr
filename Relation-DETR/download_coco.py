import os
import requests
import zipfile
from tqdm import tqdm

# COCO 2017 dataset URLs
data_urls = {
    "train_images": "http://images.cocodataset.org/zips/train2017.zip",
    "val_images": "http://images.cocodataset.org/zips/val2017.zip",
    # "test_images": "http://images.cocodataset.org/zips/test2017.zip",
    "annotations": "http://images.cocodataset.org/annotations/annotations_trainval2017.zip",
}

# Directory to save dataset
data_dir = "/mnt/sagemaker-nvme/coco2017"
os.makedirs(data_dir, exist_ok=True)

def download_file(url, dest_folder):
    local_filename = os.path.join(dest_folder, url.split("/")[-1])
    
    # Download with a progress bar
    with requests.get(url, stream=True) as r:
        total_size = int(r.headers.get('content-length', 0))
        with open(local_filename, 'wb') as f, tqdm(
            desc=local_filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))
    
    return local_filename

def unzip_file(zip_path, extract_folder):
    print(f"Unzipping {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"Unzipped {zip_path} to {extract_folder}")

def remove_file(file_path):
    if os.path.exists(file_path):
        print(f"Removing {file_path}...")
        os.remove(file_path)

# Download, unzip, and remove zip files
for name, url in data_urls.items():
    print(f"Downloading {name}...")
    zip_file_path = download_file(url, data_dir)
    
    # Unzip the downloaded file
    unzip_file(zip_file_path, data_dir)
    
    # Remove the zip file after unzipping
    remove_file(zip_file_path)

print("COCO 2017 dataset downloaded, unzipped, and zip files removed.")

