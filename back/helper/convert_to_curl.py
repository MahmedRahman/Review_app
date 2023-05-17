import json
from flask import request, jsonify 




def get_curl_command(item):
    request_data = item['request']
    url = request_data['url']['raw']
    method = request_data['method']
    headers = {header['key']: header['value'] for header in request_data.get('header', [])}

    curl_command = "curl -X {method} '{url}'".format(method=method, url=url)
    for key, value in headers.items():
        curl_command += " -H '{key}: {value}'".format(key=key, value=value)
    
    body = request_data.get('body')
    if body:
        data = body.get('raw', '')
        if data:
            curl_command += " -d '{data}'".format(data=data)

    api_name = item['name']
    prompt = f"Run the '{api_name}' API with the following cURL command: {curl_command}"

    return {'api_name': api_name, 'curl': curl_command, 'prompt': prompt}

def traverse_items(items, commands):
    for item in items:
        if 'request' in item:
            commands.append(get_curl_command(item))
        if 'item' in item:
            traverse_items(item['item'], commands)

def convert_to_curl(postman_collection):
    commands = []
    traverse_items(postman_collection['item'], commands)

    return {'commands': commands}
