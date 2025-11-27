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


model_path_object = Path(config.DETECTION_MODEL_DIR) / 'best.pt'
model_path_char = Path(config.DETECTION_MODEL_DIR) / 'yolov8n_char_new.pt'

# Initialize models as None
model_object = None
model_char = None
models_loaded = False

# load pretrained DL model
try:
    # Check if files exist before loading
    if not model_path_object.exists():
        st.error(f"❌ فایل مدل پیدا نشد: {model_path_object}")
        st.info("💡 لطفا مطمئن شوید که فایل‌های weights در Liara Disk آپلود شده‌اند")
        models_loaded = False
    elif not model_path_char.exists():
        st.error(f"❌ فایل مدل کاراکتر پیدا نشد: {model_path_char}")
        st.info("💡 لطفا مطمئن شوید که فایل‌های weights در Liara Disk آپلود شده‌اند")
        models_loaded = False
    else:
        # Both files exist, try to load them
        try:
            model_object = load_model(str(model_path_object))
            model_char = load_model(str(model_path_char))
            models_loaded = True
        except Exception as load_error:
            st.error(f"❌ خطا در بارگذاری مدل: {str(load_error)}")
            models_loaded = False
            import traceback
            st.code(traceback.format_exc(), language="python")
except Exception as e:
    st.error(f"❌ خطا در بررسی مسیر مدل: {str(e)}")
    st.error(f"مسیر بررسی شده: {model_path_object}")
    models_loaded = False
    import traceback
    st.code(traceback.format_exc(), language="python")

# image/video options
st.sidebar.header("تنظیمات تصویر/ویدیو")
source_selectbox = st.sidebar.selectbox(
    "انتخاب منبع",
    config.SOURCES_LIST
)

# Only proceed if models are loaded successfully - DOUBLE CHECK to prevent NameError
if not models_loaded or model_object is None or model_char is None:
    st.warning("⚠️ لطفا ابتدا مدل‌ها را بارگذاری کنید. فایل‌های weights باید در مسیر `/app/weights/` موجود باشند.")
    st.info("""
    **راهنمای آپلود weights در Liara:**
    1. بعد از deploy، به Liara Dashboard بروید
    2. به بخش Disks بروید
    3. disk با نام "weights" را پیدا کنید
    4. فایل‌های `best.pt` و `yolov8n_char_new.pt` را آپلود کنید
    5. اپلیکیشن را restart کنید
    """)
    # CRITICAL: Stop execution here - don't call any inference functions
    st.stop()
else:
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