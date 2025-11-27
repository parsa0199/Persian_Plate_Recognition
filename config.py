#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     config.py
   @Author:        Luyao.zhang
   @Date:          2023/5/16
   @Description: configuration file
-------------------------------------------------
"""
from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Use absolute path for better compatibility across different environments
# Try relative path first, fallback to absolute if relative fails
try:
    ROOT = root_path.relative_to(Path.cwd())
except ValueError:
    # If relative path fails (e.g., different drives on Windows or server issues), use absolute
    ROOT = root_path

print(f"ROOT path: {ROOT}")
print(f"Working directory: {Path.cwd()}")
# Source
SOURCES_LIST = ["تصویر", "ویدیو", "وبکام"]


# DL model config - use absolute path for reliability
# Try multiple path resolution methods for maximum compatibility
DETECTION_MODEL_DIR = Path('/app/weights')  # Direct absolute path for Docker/Liara
if not DETECTION_MODEL_DIR.exists():
    # Fallback to relative path from config file
    DETECTION_MODEL_DIR = root_path / 'weights'
print(f"DETECTION_MODEL_DIR: {DETECTION_MODEL_DIR}")
print(f"DETECTION_MODEL_DIR exists: {DETECTION_MODEL_DIR.exists()}")
#print(DETECTION_MODEL_DIR)
YOLOv8n = DETECTION_MODEL_DIR / "yolov8n_char_new.pt"
YOLOv8s = DETECTION_MODEL_DIR / "best.pt"



DETECTION_MODEL_LIST = [
    "yolov8n.pt",
    "yolov8s.pt"]


OBJECT_COUNTER = None
OBJECT_COUNTER1 = None