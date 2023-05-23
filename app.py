import os
from flask import Flask
from dotenv import load_dotenv
from front.routes.routes import route
from user_table import UserTable

from back.app_review.review_end_point import endpoint_app_review
from back.app_postman.postman_end_point import endpoint_postman_app
from user_table_end_point import endpoint_user_table

app = Flask(__name__)

# Load environment variables
load_dotenv()
openai_api_key = os.environ["OPENAIAPIKEY"]

app.register_blueprint(route)

app.register_blueprint(endpoint_app_review)
app.register_blueprint(endpoint_postman_app)
app.register_blueprint(endpoint_user_table)



if __name__ == "__main__":
    app.run(port=8001, debug=True)
