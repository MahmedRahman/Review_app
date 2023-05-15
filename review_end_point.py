from flask import Blueprint, request, jsonify
import requests
from google_play_scraper import app as app_info, Sort, reviews_all
from requests_toolbelt.utils import dump
import requests
from dotenv import load_dotenv

import json  # import the json module

endpoint = Blueprint('endpoint', __name__)

@endpoint.route('/generate_reply', methods=['POST'])
def generate_reply():
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
        return jsonify({'reply': friendly_reply})
    else:
        return jsonify({'error': 'Error generating friendly reply.', 'details': error_message}), 500


@endpoint.route("/scrape", methods=["GET"])
def scrape():
    #... Your existing code here ...
    app_id = request.args.get("app_id")

    if not app_id:
        return jsonify({"error": "app_id is required"}), 400

    app_details = app_info(app_id)
    rating = app_details["score"]
    total_ratings = app_details["ratings"]

    reviews = reviews_all(
        app_id,
        sleep_milliseconds=0,
        lang="en",
        country="us",
        sort=Sort.MOST_RELEVANT,
    )

    review_data = []
   

    for review in reviews:
        review_data.append({
            "author": review["userName"],
            "date": review["at"].strftime("%Y-%m-%d"),
            "review_text": review["content"],
        })

    review_data = review_data[:10]

    data = {
        "rating": rating,
        "total_ratings": total_ratings,
        "reviews": review_data,
    }

    return jsonify(data)


