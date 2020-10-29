import json
import boto3
import os
from flask import Flask,request

app = Flask(__name__)

@app.route("/get_menkui",methods=["POST","GET"])
def get_menkui():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    if os.environ.get("IS_LOCAL") == "true":
        session = boto3.session.Session(profile_name=os.environ.get("PROFILE_NAME"))
        s3_client = session.client("s3")
    else:
        s3_client = boto3.client("s3") 
    
    image_bucket_name = os.environ.get("IMAGE_BUCKET_NAME")
    key = "hogehoge.txt"
    s3_client.put_object(
        Body="file",
        Bucket=image_bucket_name,
        Key=key
    )
    url = s3_client.generate_presigned_url('get_object',Params={'Bucket': image_bucket_name,'Key': key})
    response = {
        "statusCode": 200,
        "body": json.dumps(url)
    }
    return url