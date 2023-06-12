import base64

from urllib.parse import unquote

import boto3


def encode_data(data):
    msg_bytes = data.encode("ascii")
    b64_bytes = base64.b64encode(msg_bytes)
    print(b64_bytes)


def kms_decrypt(data):
    try:
        blob = base64.decode(data)
    except ValueError as error:
        print(error)


encode_data("my key")
