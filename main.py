import os
from flask import request
from flask import json
from flask import Response
from flask_cors import CORS
from flask_api import FlaskAPI

APP = FlaskAPI(__name__)
CORS(APP)

STATUS = "STATUS"
ERROR_FILES_LIST = "ERROR_FILES_LIST"
FILES_RECEIVED_LIST = "FILES_LIST"
LABELS_MAPPING = "labels_mapping"


@APP.route("/getJsonFromFile/<filename>", methods=['GET'])
def get_json_response(filename):
    """sends json as a response for the file which contains name to number
    mapping and returns"""
    labels_dict = {}
    response_dict = {}
    try:
        with open(filename, 'r') as labels:
            labels_dict = json.load(labels)
        js_dump = json.dumps(labels_dict)
        resp = Response(js_dump,
                        status=200,
                        mimetype='application/json')

    except FileNotFoundError as err:
        print("FileNotFoundError in downloadLabel", err)
        # response_dict[STATUS] = "false"
        response_dict = {'error': 'file not found in server'}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,
                        status=500,
                        mimetype='application/json')
        print("sending error response")
    except RuntimeError as err:
        print("RuntimeError error in downloadLabel", err)
        # response_dict[STATUS] = "false"
        response_dict = {
            'error': 'error occured on server side. Please try again'}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,
                        status=500,
                        mimetype='application/json')
    return resp


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)
