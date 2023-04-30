# app.py
from flask import Flask, request, jsonify
from google_play_scraper import app as app_info, Sort, reviews_all
from flask import render_template


app = Flask(__name__)

# app.py


@app.route("/")
def index():
    return render_template("index.html")



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

    data = {
        "rating": rating,
        "total_ratings": total_ratings,
        "reviews": review_data,
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
