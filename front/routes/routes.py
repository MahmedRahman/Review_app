from flask import Blueprint, render_template,Flask,  render_template, request, jsonify
import json
from back.app_postman.postman_end_point  import convert_to_curl

route = Blueprint('route', __name__)

@route.route("/")
def index():
    return render_template("index.html")

@route.route('/about')
def about():
    return render_template('about.html')

@route.route('/contact')
def contact():
    return render_template('contact.html')

@route.route('/upload')
def upload_file_view():
    return render_template('upload.html')

@route.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_contents = file.read().decode('utf-8')
        collection = json.loads(file_contents)
        curl_commands = convert_to_curl(collection)
        return jsonify(curl_commands)
