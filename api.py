import json
import boto3
import cv2
import numpy as np
from PIL import Image
import os
from flask import Flask,request
import io
from utils.face import mosaic,get_face_positions,get_format
from botocore.exceptions import ClientError

app = Flask(__name__)

@app.route("/get_menkui",methods=["POST"])
def get_menkui():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    ALLOWED_FILE_TYPE = ["image/jpeg","image/png"]
    if request.methods != "POST":
        return {"error_msg":"request method is invalid"},405
    #TODO: EncType
    #get image data
    
    # TODO: filename encoding
    file = request.files["image"]
    if not file:
        return {"error_msg":"file is empty"},400
        
    if not(file.content_type in ALLOWED_FILE_TYPE):
        return {"error_msg":"file format is not accepted"},400

    image_data = file.read()
    # 
    if os.environ.get("IS_LOCAL") == "true":
        session = boto3.session.Session(profile_name=os.environ.get("PROFILE_NAME"))
        s3_client = session.client("s3")
    else:
        s3_client = boto3.client("s3") 

    img = np.array(Image.open(io.BytesIO(image_data))) 
    faces = get_face_positions(img)

    for (x, y, w, h) in faces:
        img = mosaic(img,x,y,w,h)
    
    # Convert Numpy array to Binary
    mosaiced_image_pillow = Image.fromarray(img)
    byte_stream = io.BytesIO()
    mosaiced_image_pillow.save(byte_stream,format=get_format(file.content_type))

    image_bucket_name = os.environ.get("IMAGE_BUCKET_NAME")
    try:
        key = file.filename
        s3_client.put_object(
            Body=byte_stream.getvalue(),
            Bucket=image_bucket_name,
            Key=key,
            ContentType=file.content_type
        )
        url = s3_client.generate_presigned_url('get_object',Params={'Bucket': image_bucket_name,'Key': key},ExpiresIn=604800) # 7 days
    except ClientError as e:
        print(e)
        return {"error_msg":"failed put object to s3"},500

    return url,201