import os
from flask import Flask
from dotenv import load_dotenv
from routes.routes import route
from back.app_review.review_end_point import endpoint_app_review
from back.app_postman.postman_end_point import endpoint_postman_app
from back.user_table.user_table_end_point import endpoint_user_tabel_app

app = Flask(__name__)

# Load environment variables
load_dotenv()
openai_api_key = os.environ["OPENAIAPIKEY"]

app.register_blueprint(route)
app.register_blueprint(endpoint_app_review)
app.register_blueprint(endpoint_postman_app)
app.register_blueprint(endpoint_user_tabel_app)



if __name__ == "__main__":
    app.run(port=8001, debug=True)
