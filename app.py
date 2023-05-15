from flask import Flask
from dotenv import load_dotenv
from helper.convert_to_curl import convert_to_curl
from postman_end_point import generate_response
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
openai_api_key = os.environ["OPENAIAPIKEY"]

from review_end_point import endpoint
from routes.routes import route

app.register_blueprint(endpoint)
app.register_blueprint(route)
app.route('/convert_to_curl', methods=['POST'])(convert_to_curl)
app.route('/explainapi', methods=['POST'])(generate_response)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
