# تشخیص پلاک خودرو (Persian Plate Recognition)
Recognize Persian plate with YOLOv8

This Repo created for detect persian cars and plates and then recognize every persian characters on the plate.

## Features

- **Detection Mode**: Detect and recognize Persian license plates from images, videos, or webcam
- **Compare Mode**: Compare detected plates with a list of valid plates from CSV file
  - Exact match: Compares full plate number including characters
  - Number match: Compares only numbers if exact match not found
- **Multiple Input Sources**: 
  - Image upload
  - Video upload
  - Real-time webcam processing
- **Persian Language Interface**: Fully localized Persian/Farsi user interface
- **Real-time Processing**: Live detection and comparison from webcam feed

## Prerequisite
YOLOv8 Ultralytics and all of Requirements for YOLOv8

use python 3.10


## Demo



https://github.com/shahabbai/PersianPlateRecog/assets/133869713/ba761742-4dfa-4f29-a016-e3876cf0d8cf




## Installation

### Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install ultralytics==8.0.104
pip install streamlit
pip install pandas
pip install opencv-python
```

## Usage

### Option 1: Command Line Script
Run the main Python script to process video/image files:
```bash
python main.py
```
The script will process `assets/video.mp4` (or image) and save results to `output/` folder.

**Note**: The script works without GUI support - it will save output files even if display is not available.

### Option 2: Streamlit Web Application (Recommended)

Run the Streamlit app locally:
```bash
streamlit run app.py
```

The app will open in your browser with a fully Persian interface.

#### Features in Streamlit App:

**1. Detection Mode (تشخیص)**
- Upload an image or video
- Use webcam for real-time detection
- View detected plates with character recognition
- Results show detected plate numbers

**2. Compare Mode (مقایسه)**
- Upload a CSV file with valid plate numbers (see `valid_plates.csv` for format)
- Upload an image or use webcam
- Compare detected plates with valid plates
- Results show:
  - ✅ **Valid**: Plate matches (exact match or number match)
  - ❌ **Unrecognized Car**: Plate doesn't match any valid plates
  - Match type: Exact match (تطابق کامل) or Number match (تطابق اعداد)

#### CSV File Format for Compare Mode

Create a CSV file with valid plate numbers:
```csv
plate_number
11b22241
12h33243
13d44565
```

The CSV should have a column named `plate_number` with valid Persian plate numbers.

### Option 3: Online Streamlit App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shahabbai-persianplaterecog-app-84qgn4.streamlit.app/)
## Datasets
Created two datasets :

1. Dataset for detection cars and plates [Link](https://universe.roboflow.com/shahab-jafari-1vorv/persian-car)

2. Dataset for detection chars of the plates [Link](https://universe.roboflow.com/shahab-jafari-1vorv/persian-plate-characters-mvinj)
## Models

For simplicity of computational using:
- **YOLOv8s** (`best.pt`): For cars and plates detection
- **YOLOv8n** (`yolov8n_char_new.pt`): For character detection on plates

Model weights should be placed in the `weights/` directory.

## Project Structure

```
Persian_Plate_Recognition/
├── app.py                 # Streamlit web application
├── main.py                # Command line script
├── utils.py               # Utility functions
├── config.py              # Configuration file
├── requirements.txt       # Python dependencies
├── valid_plates.csv       # Sample CSV for valid plates
├── assets/                # Input images/videos
│   ├── video.mp4
│   ├── car.jpg
│   └── plate.jpg
├── weights/               # Model weights
│   ├── best.pt
│   └── yolov8n_char_new.pt
└── output/                # Output directory
    └── output_*.mp4
    └── output_*.jpg
```

## Comparison Logic

The Compare mode uses a two-step matching process:

1. **Exact Match**: First checks if the detected plate exactly matches any plate in the CSV (including all characters and numbers)
2. **Number Match**: If no exact match is found, extracts only numbers from both detected and valid plates and compares them

This allows for flexible matching when character recognition might have minor errors but numbers are correct.
## Training Results
1. yolov8s model for cars and plates detection

![results (1)](https://github.com/shahabbai/PersianPlateRecog/assets/133869713/8cb0e04b-edc9-4f2a-b560-3daec538af6c)

2. yolov8n model for characters detection



![yolov8n_char_new_small](https://github.com/shahabbai/PersianPlateRecog/assets/133869713/59db56cf-94a4-4289-ad60-b8f58225b7c2)

