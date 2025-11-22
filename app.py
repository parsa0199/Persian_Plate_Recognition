#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     app.py
   @Author:        Luyao.zhang
   @Date:          2023/5/15
   @Description:
-------------------------------------------------
"""
from pathlib import Path
import streamlit as st

import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam, infer_compare

# Add Persian font styling (RTL layout)
st.markdown("""
    <style>
        /* Persian Font */
        * {
            font-family: 'Tahoma', 'Arial', 'DejaVu Sans', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# setting page layout
st.set_page_config(
    page_title="تشخیص پلاک خودرو",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# main page heading
st.title("🚗 تشخیص پلاک خودرو")

# sidebar
st.sidebar.header("تنظیمات مدل")

# model options
task_type = st.sidebar.selectbox(
    "انتخاب کار",
    ["تشخیص", "مقایسه"]
)

# model_type = None
# if task_type == "Detection":
#     model_type = st.sidebar.selectbox(
#         "Select Model",
#         config.DETECTION_MODEL_LIST
#     )
# else:
#     st.error("Currently only 'Detection' function is implemented")

confidence = float(st.sidebar.slider(
    "انتخاب دقت مدل", 30, 100, 50)) / 100


model_path_object = Path(config.DETECTION_MODEL_DIR, 'best.pt')
print(model_path_object)
model_path_char = Path(config.DETECTION_MODEL_DIR, 'yolov8n_char_new.pt')

 

# load pretrained DL model
try:

    
    model_object = load_model(model_path_object)
    model_char = load_model(model_path_char)
except Exception as e:
    st.error(f"نمیتوان مدل را بارگیری کرد. لطفا مسیر مشخص شده را بررسی کنید: {model_path_object}")

# image/video options
st.sidebar.header("تنظیمات تصویر/ویدیو")
source_selectbox = st.sidebar.selectbox(
    "انتخاب منبع",
    config.SOURCES_LIST
)

source_img = None
if task_type == "مقایسه":
    # For Compare task, use the compare function with source selection
    if source_selectbox == config.SOURCES_LIST[0]: # تصویر
        infer_compare(confidence, model_object, model_char, source_type="Image")
    elif source_selectbox == config.SOURCES_LIST[2]: # وبکام
        infer_compare(confidence, model_object, model_char, source_type="Webcam")
    else:
        st.info("برای مقایسه، لطفا 'تصویر' یا 'وبکام' را انتخاب کنید")
elif task_type == "تشخیص":
    # For Detection task, use the original functions
    if source_selectbox == config.SOURCES_LIST[0]: # تصویر
        infer_uploaded_image(confidence, model_object, model_char)
    elif source_selectbox == config.SOURCES_LIST[1]: # ویدیو
        infer_uploaded_video(confidence, model_object, model_char)
    elif source_selectbox == config.SOURCES_LIST[2]: # وبکام
        infer_uploaded_webcam(confidence, model_object, model_char)
    else:
        st.error("فقط 'تصویر' و 'ویدیو' مناسب هستند")