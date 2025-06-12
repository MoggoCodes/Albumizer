# Albumizer

A Python application for swapping faces in album cover art using InsightFace.

## Requirements

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

## Directory Structure

The application uses a specific directory structure for organizing images:

- `Photos/People/`: Store your source face images here
- `Photos/Albums/`: Store your target album covers here
- `Photos/Swapped/`: Generated face-swapped images will be saved here
- `models/`: Contains downloaded AI models

## Usage

1. Place your source face image in the `Photos/People/` directory
2. Place your target album cover in the `Photos/Albums/` directory
3. Run the face swapper:

```bash
# Basic usage
pixi run python face_swapper.py source_image.jpg album_cover.jpg

# With custom output filename
pixi run python face_swapper.py source_image.jpg album_cover.jpg -o result.png
```

### Examples

```bash
# Using default output naming (source_on_target.png)
pixi run python face_swapper.py me.jpg dark_side_of_the_moon.jpg

# Specifying custom output name
pixi run python face_swapper.py me.jpg abbey_road.jpg -o me_abbey_road.png
```

The swapped image will be saved in the `Photos/Swapped/` directory.

## Project Structure

- `face_swapper.py`: Main script for face swapping
- `download_models.py`: Script to download required AI models
- `models/`: Directory containing downloaded AI models
- `pixi.toml`: Pixi dependency configuration
- `pixi.lock`: Pixi lock file

## License

MIT License
