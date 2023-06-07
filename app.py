# save this as app.py
import boto3
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    string = "dfghj"
    encoded_string = string.encode("utf-8")

    bucket_name = "krkn-telemetry"
    file_name = "hello.txt"

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=encoded_string)
    return "Hello, World cazzo mimmo!"