import json
import boto3
import os

def get_menkui(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    session = boto3.session.Session(profile_name="yadayuki")
    s3_client = session.client("s3")
    image_bucket_name = os.environ.get("IMAGE_BUCKET_NAME")
    res = s3_client.put_object(
        Body="file",
        Bucket=image_bucket_name,
        Key="sample.txt"
    )
    print(res)
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
