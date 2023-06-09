# save this as app.py
import os
import boto3
import json
import uuid
from krkn_lib_kubernetes import ChaosRunTelemetry
from flask import Flask, Response, request
from types import SimpleNamespace
app = Flask(__name__)


@app.route("/", methods=['POST'])
def telemetry():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        try:
            bucket_name = os.getenv("BUCKET_NAME")
            if bucket_name is None:
                return Response("BUCKET_NAME env variable not set", status=500)
            telemetry_data = ChaosRunTelemetry(request.json)
            validation_response = validate_data_model(telemetry_data)
            # if validator returns means that there are validation errors
            if validation_response is not None:
                return validation_response
            uuid_str = str(uuid.uuid4())
            file_name = f"{uuid_str}.json"
            s_three = boto3.resource("s3")
            telemetry_str = json.dumps(
                telemetry_data, default=lambda o: o.__dict__, indent=4
            )
            s_three.Bucket(bucket_name).put_object(Key=file_name, Body=telemetry_str)
            return Response(f"record {uuid_str} created test")
        except Exception as e:
            return Response(f"[bad request]: {str(e)}", status=400)
    else:
        return Response("content type not supported", status=415)


def validate_data_model(model:  ChaosRunTelemetry) -> Response :
    for scenario in model.scenarios:
        for attr, _ in scenario.__dict__.items():
            if attr != "parameters":
                if getattr(scenario, attr) is None:
                    return Response(f"[bad request]: {attr} must be set")
            else:
                if getattr(scenario, attr) is not None or getattr(scenario, attr) != "":
                    return Response("[bad request]: parameters cannot be set")



