import streamlit as st
import time
from PIL import Image
import numpy as np
import torch
from detect import detect
import cv2
# Header

st.markdown("# Playing Cards Detection")

st.text("This project aims to detect the playing card number with their type")
st.text("This project made using YOLOV5 algorithms, and trained with more than 25K of data.")

st.markdown(' <br> <h2 style="text-align:center">Try Your Cards!</h2>',unsafe_allow_html=True)


# Define & Make Columns

col1, col2, col3, col4, = st.columns(4)


with col1:
    upload_photo = st.button("Upload photo")
    
with col2:
    live_photo = st.button("Take a photo")
    
with col3:
    upload_video = st.button("Upload video")
    
with col4:
    live_video = st.button("Live webcam")
    
# Section 2:


# Check Compatible Files
image = st.file_uploader("asfd", type=['jpg','png','jpeg'])
if image is not None:
    show_image = Image.open(image)
    img_array = np.array(show_image)
    st.image(img_array)
#def check_image(img):
    
# Check Buttons
if upload_photo :
    image = st.file_uploader("", type=['jpg','png','jpeg'])
    
#     def check_image(img):
        
#         if image:
#             lst = str(img).split(',')
#             img_name = lst[1][7:-1]
        
        
#         correct = ['jpg','png']
#         if img_name.split('.')[-1] in correct:
#             return True
#         else:
#             st.error("The File not in photo format. Please input compatible picture format like .png .jpg")
            
    #if check_image(image):
    #    python .\detect.py --weights best_weights.pt --img 640 --conf 0.25 --source image
        
    if image is not None:
        show_image = Image.open(image)
        st.image(show_image)
    
if live_photo :
    image = st.camera_input("")
    
if upload_video :
    video = st.file_uploader("")
    if video:
        lst = str(video).split(',')
        file_name = lst[1][7:-1]
        
        if file_name[-4:] != '.mp4':
            st.error("File type is not compatible, please upload .mp4 file")
        else:
            pass
            
    
if live_video :
    live = st.camera_input("")



    

