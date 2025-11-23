#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     utils.py
   @Author:        Luyao.zhang
   @Date:          2023/5/16
   @Description:
-------------------------------------------------
"""
from ultralytics import YOLO
import streamlit as st
import cv2
from PIL import Image
import tempfile
import config
import pandas as pd
import re
import io


charclassnames = ['0','9','b','d','ein','ein','g','gh','h','n','s','1','malul','n','s','sad','t','ta','v','y','2'
                  ,'3','4','5','6','7','8']



def _display_detected_frames(conf, model_object, model_char, st_count, st_frame, image):
    """
    Display the detected objects on a video frame using the YOLOv8 model.
    :param conf (float): Confidence threshold for object detection.
    :param model (YOLOv8): An instance of the `YOLOv8` class containing the YOLOv8 model.
    :param st_frame (Streamlit object): A Streamlit object to display the detected video.
    :param image (numpy array): A numpy array representing the video frame.
    :return: None
    """
    # Resize the image to a standard size
    #image = cv2.resize(image, (720, int(720 * (9 / 16))))

    # Predict the objects in the image using YOLOv8 model
    res_object = model_object.predict(image, conf=conf)
    char_result = ''  # Initialize char_result to avoid UnboundLocalError
    for i in res_object:
        bbox = i.boxes
        for box in bbox:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            #confs = math.ceil((box.conf[0]*100))/100
            cls_names = int(box.cls[0])
            

            #check plate to recognize characters with yolov8n model
            if cls_names == 1:
                char_display = []
                #crop plate from frame
                plate_img = image[y1:y2, x1:x2]
                #plate_img = uploaded_image[y1:y2, x1:x2]
                #detect characters of plate with yolov8n model
                plate_output = model_char(plate_img, conf=0.4)
                
                #extract bounding box and class names
                bbox = plate_output[0].boxes.xyxy
                cls = plate_output[0].boxes.cls
                #make a dict and sort it from left to right to show the correct characters of plate
                keys = cls.numpy().astype(int)
                values =bbox[:, 0].numpy().astype(int)
                dictionary = list(zip(keys, values))
                sorted_list = sorted(dictionary, key=lambda x: x[1])
                #convert all characters to a string
                for i in sorted_list:
                    char_class = i[0]
                    #char_display.append(plate_output[0].names[char_class])
                    char_display.append(charclassnames[char_class])
                char_result ='Plate: ' + (''.join(char_display))
    
                #just show the correct characters in output
    
    inText = 'Vehicle In'
    outText = 'Vehicle Out'
    if config.OBJECT_COUNTER1 != None:
        for _, (key, value) in enumerate(config.OBJECT_COUNTER1.items()):
            inText += ' - ' + str(key) + ": " +str(value)
    if config.OBJECT_COUNTER != None:
        for _, (key, value) in enumerate(config.OBJECT_COUNTER.items()):
            outText += ' - ' + str(key) + ": " +str(value)
    
    st.markdown(
    f'<style>img {{ max-width: {640}px; height: auto; }}</style>',
    unsafe_allow_html=True
)
    # Plot the detected objects on the video frame
    st_count.write(inText + '\n\n' + outText)
    res_plotted = res_object[0].plot()
    st_frame.image(res_plotted,
                   caption='ویدیو تشخیص داده شده',
                   channels="BGR",
                   width='stretch'
                   )
    text_placeholder = st.empty()
    if char_result:  # Only display if a plate was detected
        text_placeholder.markdown(f"**{char_result}**")
    #st.write(char_result)


@st.cache_resource
def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def infer_uploaded_image(conf, model_object, model_char):
    """
    Execute inference for uploaded image
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    source_img = st.sidebar.file_uploader(
        label="انتخاب تصویر...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            uploaded_image = Image.open(source_img)
            # adding the uploaded image to the page with caption
            st.image(
                image=source_img,
                caption="تصویر بارگذاری شده",
                width='stretch'
            )

    if source_img:
        if st.button("🔍 اجرای تشخیص"):
            with st.spinner("در حال پردازش..."):
                res_object = model_object.predict(uploaded_image,
                                    conf=conf)
                boxes = res_object[0].boxes
                    #extract bounding box and class names
                res_plotted = res_object[0].plot()[:, :, ::-1]
                char_display = []  # Initialize char_display to avoid UnboundLocalError
                char_result = ''  # Initialize char_result to avoid UnboundLocalError
                for i in res_object:
                    bbox = i.boxes
                    for box in bbox:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        #confs = math.ceil((box.conf[0]*100))/100
                        cls_names = int(box.cls[0])
                        

                        #check plate to recognize characters with yolov8n model
                        if cls_names == 1:
                            char_display = []  # Reset for each plate
                            #crop plate from frame
                            plate_img = uploaded_image.crop((x1, y1, x2, y2))
                            #plate_img = uploaded_image[y1:y2, x1:x2]
                            #detect characters of plate with yolov8n model
                            plate_output = model_char(plate_img, conf=0.4)
                            
                            #extract bounding box and class names
                            bbox = plate_output[0].boxes.xyxy
                            cls = plate_output[0].boxes.cls
                            #make a dict and sort it from left to right to show the correct characters of plate
                            keys = cls.numpy().astype(int)
                            values =bbox[:, 0].numpy().astype(int)
                            dictionary = list(zip(keys, values))
                            sorted_list = sorted(dictionary, key=lambda x: x[1])
                            #convert all characters to a string
                            for i in sorted_list:
                                char_class = i[0]
                                #char_display.append(plate_output[0].names[char_class])
                                char_display.append(charclassnames[char_class])
                            char_result ='Plate: ' + (''.join(char_display))
                
                            #just show the correct characters in output
                

                with col2:
                    st.image(res_plotted,
                             caption="تصویر تشخیص داده شده",
                             width='stretch')
                    if char_result and len(char_display) == 8:  # Only display if plate was detected and has 8 characters
                        st.write(f"**{char_result}**")
                    try:
                        with st.expander("نتایج تشخیص"):
                            for box in boxes:
                                st.write(box.xywh)
                    except Exception as ex:
                        st.write("هنوز تصویری بارگذاری نشده است!")
                        st.write(ex)


def infer_uploaded_video(conf, model_object, model_char):
    """
    Execute inference for uploaded video
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    source_video = st.sidebar.file_uploader(
        label="انتخاب ویدیو..."
    )

    if source_video:
        st.markdown(
    f'<style>video {{ width: {640}px !important; height: auto !important; }}</style>',
    unsafe_allow_html=True
)
        st.video(source_video)

    if source_video:
        if st.button("🔍 اجرای تشخیص"):
            with st.spinner("در حال پردازش..."):
                try:
                    
                    tfile = tempfile.NamedTemporaryFile()
                    tfile.write(source_video.read())
                    vid_cap = cv2.VideoCapture(
                        tfile.name)
                    st_count = st.empty()
                    st_frame = st.empty()
                    while (vid_cap.isOpened()):
                        success, image = vid_cap.read()
                        if success:
                            _display_detected_frames(conf,
                                                     model_object,model_char,
                                                     st_count,
                                                     st_frame,
                                                     image
                                                     )
                        else:
                            vid_cap.release()
                            break
                except Exception as e:
                    st.error(f"خطا در بارگذاری ویدیو: {e}")


def infer_uploaded_webcam(conf, model_object, model_char):
    """
    Execute inference for webcam.
    :param conf: Confidence of YOLOv8 model
    :param model: An instance of the `YOLOv8` class containing the YOLOv8 model.
    :return: None
    """
    try:
        flag = st.button(
            label="⏹️ توقف"
        )
        vid_cap = cv2.VideoCapture(0)  # local camera
        st_count = st.empty()
        st_frame = st.empty()
        while not flag:
            success, image = vid_cap.read()
            if success:
                _display_detected_frames(
                    conf,
                    model_object,
                    model_char,
                    st_count,
                    st_frame,
                    image
                )
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.error(f"خطا در بارگذاری ویدیو: {str(e)}")


def extract_numbers(plate_string):
    """
    Extract only numbers from a plate string
    :param plate_string: String containing plate characters and numbers
    :return: String containing only numbers
    """
    return re.sub(r'[^0-9]', '', plate_string)


def load_valid_plates(csv_file):
    """
    Load valid plate numbers from CSV file
    :param csv_file: Uploaded CSV file object
    :return: List of valid plate numbers
    """
    try:
        df = pd.read_csv(csv_file)
        # Handle different possible column names
        if 'plate_number' in df.columns:
            plates = df['plate_number'].astype(str).tolist()
        elif 'plate' in df.columns:
            plates = df['plate'].astype(str).tolist()
        else:
            # Use first column if standard names not found
            plates = df.iloc[:, 0].astype(str).tolist()
        return [plate.strip().lower() for plate in plates if plate.strip()]
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return []


def compare_plate(detected_plate, valid_plates):
    """
    Compare detected plate with valid plates
    :param detected_plate: Detected plate string
    :param valid_plates: List of valid plate numbers
    :return: Tuple (status, match_type) where status is 'valid' or 'unrecognized car'
    """
    detected_plate = detected_plate.lower().strip()
    
    # First: Check for exact match (including characters)
    if detected_plate in valid_plates:
        return ('valid', 'exact_match')
    
    # Second: Extract numbers and compare
    detected_numbers = extract_numbers(detected_plate)
    for valid_plate in valid_plates:
        valid_numbers = extract_numbers(valid_plate)
        if detected_numbers == valid_numbers and detected_numbers:  # Make sure numbers exist
            return ('valid', 'number_match')
    
    return ('unrecognized car', 'no_match')


def infer_compare(conf, model_object, model_char, source_type="Image"):
    """
    Execute inference and comparison for uploaded image or webcam
    :param conf: Confidence of YOLOv8 model
    :param model_object: Object detection model
    :param model_char: Character recognition model
    :param source_type: Source type - "Image" or "Webcam"
    :return: None
    """
    st.header("مقایسه پلاک")
    
    # CSV file upload
    csv_file = st.sidebar.file_uploader(
        label="بارگذاری فایل CSV با پلاک‌های معتبر...",
        type=("csv",),
        help="فایل CSV باید دارای ستون 'plate_number' با شماره پلاک‌های معتبر باشد"
    )
    
    if source_type == "Webcam":
        # For webcam, use the webcam comparison function
        infer_compare_webcam(conf, model_object, model_char, csv_file)
        return
    
    # For image upload
    source_img = st.sidebar.file_uploader(
        label="انتخاب تصویر...",
        type=("jpg", "jpeg", "png", 'bmp', 'webp')
    )

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            uploaded_image = Image.open(source_img)
            st.image(
                image=source_img,
                caption="تصویر بارگذاری شده",
                width='stretch'
            )

    if source_img and csv_file:
        if st.button("🔍 مقایسه"):
            with st.spinner("در حال مقایسه..."):
                # Load valid plates
                valid_plates = load_valid_plates(csv_file)
                
                if not valid_plates:
                    st.error("هیچ پلاک معتبری در فایل CSV یافت نشد. لطفا فرمت فایل را بررسی کنید.")
                    return
                
                st.success(f"✅ {len(valid_plates)} شماره پلاک معتبر از CSV بارگذاری شد")
                
                # Detect plates in image
                res_object = model_object.predict(uploaded_image, conf=conf)
                boxes = res_object[0].boxes
                res_plotted = res_object[0].plot()[:, :, ::-1]
                
                detected_plates = []
                char_display = []
                char_result = ''
                
                for i in res_object:
                    bbox = i.boxes
                    for box in bbox:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cls_names = int(box.cls[0])

                        # Check plate to recognize characters
                        if cls_names == 1:
                            char_display = []
                            plate_img = uploaded_image.crop((x1, y1, x2, y2))
                            plate_output = model_char(plate_img, conf=0.4)
                            
                            bbox = plate_output[0].boxes.xyxy
                            cls = plate_output[0].boxes.cls
                            keys = cls.numpy().astype(int)
                            values = bbox[:, 0].numpy().astype(int)
                            dictionary = list(zip(keys, values))
                            sorted_list = sorted(dictionary, key=lambda x: x[1])
                            
                            for i in sorted_list:
                                char_class = i[0]
                                char_display.append(charclassnames[char_class])
                            
                            if len(char_display) == 8:
                                detected_plate = ''.join(char_display)
                                status, match_type = compare_plate(detected_plate, valid_plates)
                                detected_plates.append({
                                    'plate': detected_plate,
                                    'status': status,
                                    'match_type': match_type
                                })
                                char_result = f'Plate: {detected_plate} - {status.upper()}'

                with col2:
                    st.image(res_plotted,
                             caption="تصویر تشخیص داده شده",
                             width='stretch')
                    
                    if detected_plates:
                        st.subheader("نتایج مقایسه")
                        for idx, plate_info in enumerate(detected_plates, 1):
                            status_color = "🟢" if plate_info['status'] == 'valid' else "🔴"
                            status_text = "معتبر" if plate_info['status'] == 'valid' else "خودرو نامعتبر"
                            match_info = ""
                            if plate_info['match_type'] == 'exact_match':
                                match_info = " (تطابق کامل)"
                            elif plate_info['match_type'] == 'number_match':
                                match_info = " (تطابق اعداد)"
                            st.write(f"{status_color} **پلاک {idx}:** {plate_info['plate']} - **{status_text}**{match_info}")
                    else:
                        if char_result:
                            st.warning("پلاک تشخیص داده شد اما با هیچ پلاک معتبری مطابقت ندارد")
                            st.write(char_result)
                        else:
                            st.info("هیچ پلاکی در تصویر تشخیص داده نشد")
                    
                    try:
                        with st.expander("نتایج تشخیص"):
                            for box in boxes:
                                st.write(box.xywh)
                    except Exception as ex:
                        st.write("هیچ نتیجه تشخیصی در دسترس نیست")
    elif source_img and not csv_file:
        st.warning("لطفا فایل CSV با شماره پلاک‌های معتبر را بارگذاری کنید")
    elif csv_file and not source_img:
        st.warning("لطفا تصویری برای مقایسه بارگذاری کنید")


def _display_compare_frames(conf, model_object, model_char, valid_plates, st_frame, st_status, image):
    """
    Display the detected objects with comparison on a video frame using the YOLOv8 model.
    :param conf (float): Confidence threshold for object detection.
    :param model_object: Object detection model
    :param model_char: Character recognition model
    :param valid_plates: List of valid plate numbers
    :param st_frame (Streamlit object): A Streamlit object to display the detected video.
    :param st_status (Streamlit object): A Streamlit object to display the comparison status.
    :param image (numpy array): A numpy array representing the video frame.
    :return: None
    """
    # Predict the objects in the image using YOLOv8 model
    res_object = model_object.predict(image, conf=conf)
    char_result = ''  # Initialize char_result to avoid UnboundLocalError
    detected_plates = []
    
    for i in res_object:
        bbox = i.boxes
        for box in bbox:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cls_names = int(box.cls[0])

            # Check plate to recognize characters
            if cls_names == 1:
                char_display = []
                # Crop plate from frame
                plate_img = image[y1:y2, x1:x2]
                # Detect characters of plate with yolov8n model
                plate_output = model_char(plate_img, conf=0.4)
                
                # Extract bounding box and class names
                bbox = plate_output[0].boxes.xyxy
                cls = plate_output[0].boxes.cls
                # Make a dict and sort it from left to right to show the correct characters of plate
                keys = cls.numpy().astype(int)
                values = bbox[:, 0].numpy().astype(int)
                dictionary = list(zip(keys, values))
                sorted_list = sorted(dictionary, key=lambda x: x[1])
                # Convert all characters to a string
                for i in sorted_list:
                    char_class = i[0]
                    char_display.append(charclassnames[char_class])
                
                if len(char_display) == 8:
                    detected_plate = ''.join(char_display)
                    status, match_type = compare_plate(detected_plate, valid_plates)
                    detected_plates.append({
                        'plate': detected_plate,
                        'status': status,
                        'match_type': match_type
                    })
                    char_result = f'Plate: {detected_plate} - {status.upper()}'
    
    # Plot the detected objects on the video frame
    res_plotted = res_object[0].plot()
    st_frame.image(res_plotted,
                   caption='ویدیو تشخیص داده شده',
                   channels="BGR",
                   width='stretch'
                   )
    
    # Display comparison results
    if detected_plates:
        status_text = ""
        for idx, plate_info in enumerate(detected_plates, 1):
            status_color = "🟢" if plate_info['status'] == 'valid' else "🔴"
            status_text_persian = "معتبر" if plate_info['status'] == 'valid' else "خودرو نامعتبر"
            match_info = ""
            if plate_info['match_type'] == 'exact_match':
                match_info = " (تطابق کامل)"
            elif plate_info['match_type'] == 'number_match':
                match_info = " (تطابق اعداد)"
            status_text += f"{status_color} **{idx}:** {plate_info['plate']} - **{status_text_persian}**{match_info}\n\n"
        st_status.markdown(status_text)
    else:
        st_status.info("هیچ پلاکی در فریم فعلی تشخیص داده نشد")


def infer_compare_webcam(conf, model_object, model_char, csv_file):
    """
    Execute inference and comparison for webcam.
    :param conf: Confidence of YOLOv8 model
    :param model_object: Object detection model
    :param model_char: Character recognition model
    :param csv_file: Uploaded CSV file with valid plates
    :return: None
    """
    if not csv_file:
        st.warning("لطفا فایل CSV با شماره پلاک‌های معتبر را بارگذاری کنید")
        return
    
    # Load valid plates
    valid_plates = load_valid_plates(csv_file)
    
    if not valid_plates:
        st.error("هیچ پلاک معتبری در فایل CSV یافت نشد. لطفا فرمت فایل را بررسی کنید.")
        return
    
    st.success(f"✅ {len(valid_plates)} شماره پلاک معتبر از CSV بارگذاری شد")
    
    try:
        flag = st.button(
            label="⏹️ توقف"
        )
        vid_cap = cv2.VideoCapture(0)  # local camera
        st_frame = st.empty()
        st_status = st.empty()
        
        while not flag:
            success, image = vid_cap.read()
            if success:
                _display_compare_frames(
                    conf,
                    model_object,
                    model_char,
                    valid_plates,
                    st_frame,
                    st_status,
                    image
                )
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.error(f"خطا در بارگذاری وبکام: {str(e)}")
