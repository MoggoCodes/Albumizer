import os
import requests
from tqdm import tqdm

def download_file(url, destination):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def main():
    # Create directories if they don't exist
    os.makedirs('models/insightface', exist_ok=True)
    os.makedirs('models/reswapper', exist_ok=True)

    # Model URLs
    models = {
        'models/insightface/inswapper_128.onnx': 
            'https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx',
        'models/reswapper/reswapper_v1.safetensors':
            'https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/reswapper/reswapper_v1_0.safetensors',
        'models/insightface/buffalo_l.zip':
            'https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/buffalo_l.zip'
    }

    # Download each model
    for dest, url in models.items():
        if not os.path.exists(dest):
            print(f"\nDownloading {os.path.basename(dest)}...")
            download_file(url, dest)
            print(f"Downloaded {os.path.basename(dest)}")
        else:
            print(f"\n{os.path.basename(dest)} already exists, skipping...")

    print("\nAll models downloaded successfully!")

if __name__ == "__main__":
    main() 