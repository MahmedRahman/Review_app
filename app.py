# app.py
import os
import requests
from flask import Flask, render_template, request, jsonify
from google_play_scraper import app as app_info, Sort, reviews_all
from flask import render_template
from dotenv import load_dotenv
from config import OPENAI_API_KEY

app = Flask(__name__)

# app.py
@app.route('/generate_reply', methods=['POST'])
def generate_reply():
    review_text = request.json.get('review_text')
    global OPENAI_API_KEY
    prompt = f'Create a friendly reply for a user facing technical difficulties. Please provide a complete response with possible solutions and contact information for further assistance in about 85 words: \n\n"{review_text}"'

    api_url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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",
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


@app.route("/scrape", methods=["GET"])
def scrape():
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


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')




if __name__ == "__main__":
    app.run(port=8000, debug=True)
