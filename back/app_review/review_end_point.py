import json  # import the json module
import requests
import requests
import os
from flask import Blueprint, request, jsonify
from google_play_scraper import app as app_info, Sort, reviews
from requests_toolbelt.utils import dump
from dotenv import load_dotenv
from back.helper.responses import create_response


endpoint_app_review = Blueprint('endpoint_app_review', __name__)

@endpoint_app_review.route('/friendly_reply', methods=['POST'])
def friendly_reply():
    review_text = request.json.get('review_text')

    load_dotenv()

    openai_api_key = os.environ["OPENAIAPIKEY"]
   
    prompt = f'''Create a friendly reply for a user. 
    Please provide a complete response in about 85 words: {review_text}'''



    api_url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 170,
        "temperature": 1,
        "n": 1,
    }

    friendly_reply = None
    error_message = None

    try:
        response = requests.post(api_url, json=data, headers=headers)

        response.raise_for_status()

        reply = response.json()["choices"][0]["text"].strip()
        friendly_reply = f"Friendly reply: {reply}"
    except requests.exceptions.RequestException as error:
        print(f"Error generating friendly reply: {error}")
        error_message = f"Error generating friendly reply: {error}"
        friendly_reply = None

    if friendly_reply is not None:
        return create_response(success=True, code=200,data=friendly_reply)
    else:
        return create_response(success=False, code=400,errors=[{"error": "Error generating friendly reply"}])


@endpoint_app_review.route("/scrape_reply", methods=["GET"])
def scrape():
    app_id = request.args.get("app_id")

    if not app_id:
        return create_response(success=False, code=400,errors=[{"error": "app_id is required"}])
       

    app_details = app_info(app_id)

    rating = app_details["score"]
    
    total_ratings = app_details["ratings"]

    result, continuation_token = reviews(
        app_id,
        count=5,
        sort=Sort.MOST_RELEVANT,
    )
   
    data = {
            "rating": rating,
            "total_ratings": total_ratings,
            "reviews": result,
         }
    
    
    return create_response(success=True, code=200,data=data)

    

   


