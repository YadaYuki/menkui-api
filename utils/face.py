import cv2
import numpy as np
from PIL import Image
import os
import io

DETECTOR_PATH = 'detector/haarcascade_frontalface_default.xml'

def mosaic_all(img,ratio=0.05):
    small = cv2.resize(img,None,fx=ratio,fy=ratio,interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small,img.shape[:2][::-1],interpolation=cv2.INTER_NEAREST)

def mosaic(img,x,y,w,h):
    dst = img.copy()
    dst[y:y+h,x:x+w] = mosaic_all(dst[y:y+h,x:x+w])
    return dst
    
def get_face_positions(img_file):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    face_cascade = cv2.CascadeClassifier(os.path.join(file_dir,DETECTOR_PATH))
    gray = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

def get_format(content_type):
    content_dict = {
        "image/jpeg":"JPEG",
        "image/png":"PNG"
    }
    return content_dict[content_type]