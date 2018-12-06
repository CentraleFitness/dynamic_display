import sys
import base64

def get_data_from_uri(uri):
    b64_data = uri.split(",")
    if len(b64_data) > 1:
    # substract only b64 data without header
        return base64.b64decode(b64_data[1])
    else:
        return base64.b64decode(b64_data[0])