import json  # import the json module
import os
import requests
from flask import Blueprint, request, jsonify 
from google_play_scraper import app as app_info, Sort, reviews, exceptions
from requests_toolbelt.utils import dump
from dotenv import load_dotenv
from back.helper.responses import create_response, extract_app_id
from urllib.parse import urlparse, parse_qs


endpoint_app_review = Blueprint('endpoint_app_review', __name__)

@endpoint_app_review.route('/friendly_reply', methods=['POST'])
def friendly_reply():
    
    review_text = request.json.get('review_text')
    
    if review_text is None:
        return create_response(success=False, code=400,errors="Missing review_text query parameter")

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
        return create_response(success=False, code=400,errors="Error generating friendly reply")


@endpoint_app_review.route("/scrape_reply", methods=["GET"])
def scrape():
    app_url = request.args.get("app_url")

    if app_url is None:
        return create_response(success=False, code=400,errors="Missing app_url query parameter")


    try:
        # Parse the URL and check if it has a scheme and netloc
        url_parts = urlparse(app_url)
        
        if not all([url_parts.scheme, url_parts.netloc]) or 'play.google.com' not in url_parts.netloc:
            return create_response(success=False, code=400,errors="not google play URL")



        app_id = extract_app_id(app_url)
        
        if app_id is 'Invalid URL':
            return create_response(success=False, code=400,errors="Invalid URL")
        
        if not app_id:
            return create_response(success=False, code=400,errors="app_id is required")
        
        try:
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
        except exceptions.NotFoundError:
            return create_response(success=False, code=400,errors="app id not found")

    except :
        return create_response(success=False, code=400,errors="error")



   

   


