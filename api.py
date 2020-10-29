import json
import boto3
import os
from flask import Flask,request

app = Flask(__name__)

@app.route("/get_menkui",methods=["POST","GET"])
def get_menkui():
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    session = boto3.session.Session(profile_name="yadayuki")
    s3_client = session.client("s3")
    image_bucket_name = os.environ.get("IMAGE_BUCKET_NAME")
    res = s3_client.put_object(
        Body="file",
        Bucket=image_bucket_name,
        Key="gehogehoge.txt"
    )
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response