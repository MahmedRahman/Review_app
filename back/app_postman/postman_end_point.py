import openai
import json
from flask import request, jsonify,Blueprint
from back.helper.convert_to_curl import convert_to_curl
from werkzeug.utils import secure_filename
import json

endpoint_postman_app = Blueprint('endpoint_postman_app', __name__)

# Global response variable
response = None

@endpoint_postman_app.route('/api/v1/generate', methods=['GET'])
def generate_single_response():
    global response
    data = request.get_json()
    try:
        prompt = data['prompt']
    except KeyError as e:
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        user="my-unique-identifier"
    )

    return jsonify({"response": response.choices[0].text.strip()})

@endpoint_postman_app.route('/api/v1/generate_batch', methods=['POST'])
def generate_multiple_responses():
    global response
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of maps"}), 400

    responses = []
    for item in data:
        try:
            api_name = item['api_name']
            curl = item['curl']
            prompt = item['prompt']
        except KeyError as e:
            return jsonify({"error": f"Missing key in item: {e.args[0]}"}), 400

        # Use the single response function
        single_response = generate_single_response()

        # Append the response text to the responses list
        responses.append({"api_name": api_name, "response": single_response})

    # Return a JSON object with all the responses
    return jsonify(responses)

@endpoint_postman_app.route('/convert_to_curl', methods=['POST'])
def convert_to_curl_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_content = file.read()
    try:
        postman_collection = json.loads(file_content)
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to decode JSON'}), 400
    try:
        commands = convert_to_curl(postman_collection)
        return jsonify(commands)
    except Exception as e:
        return jsonify({'error': 'Failed to process the data'}), 500

