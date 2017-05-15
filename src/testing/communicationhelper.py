import json
import requests

def build_json_header_and_payload(payload=None):

    headers = None
    json_payload = None

    if payload != None:
        headers = {'Content-Type' : 'application/json'}
        json_payload = json.dumps(payload)

    return (headers, json_payload)

def get_json(url):

    response = requests.get(url)

    return json.loads(response.content.decode())

def post_json(url, payload=None):

    (headers, payload) = build_json_header_and_payload(payload)
    response = requests.post(url, data=payload, headers=headers)

    return json.loads(response.content.decode())

def put_json(url, payload=None):

    (headers, payload) = build_json_header_and_payload(payload)
    response = requests.put(url, data=payload, headers=headers)

    return json.loads(response.content.decode())
