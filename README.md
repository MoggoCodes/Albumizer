# Albumizer

A Python application for swapping faces in album cover art using InsightFace.

## Requirements

- Python 3.13 or higher
- Pixi package manager

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Albumizer
```

2. Install dependencies using Pixi:
```bash
pixi install
```

3. Download the required models:
```bash
pixi run python download_models.py
```

## Usage

1. Place your source image (the face you want to use) in the project directory as `Headshot.JPG`
2. Place your target album cover in the project directory as `jam.jpg`
3. Run the face swapper:
```bash
pixi run python face_swapper.py
```
4. The result will be saved as `face_swapped_album.png`

## Project Structure

- `face_swapper.py`: Main script for face swapping
- `download_models.py`: Script to download required AI models
- `models/`: Directory containing downloaded AI models
- `pixi.toml`: Pixi dependency configuration
- `pixi.lock`: Pixi lock file

## License

MIT License
