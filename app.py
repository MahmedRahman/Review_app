import os
from flask import Flask
from dotenv import load_dotenv
from front.routes.routes import route
from back.app_review.review_end_point import endpoint_app_review
from back.app_postman.postman_end_point import endpoint_postman_app

app = Flask(__name__)

# Load environment variables
load_dotenv()
openai_api_key = os.environ["OPENAIAPIKEY"]

app.register_blueprint(route)
app.register_blueprint(endpoint_app_review)
app.register_blueprint(endpoint_postman_app)



if __name__ == "__main__":
    app.run(port=8001, debug=True)
