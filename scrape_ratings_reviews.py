import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from google_play_scraper import app, Sort, reviews_all
import json

app_id = "com.spade.mekapp"

app_info = app(app_id)
rating = app_info["score"]
total_ratings = app_info["ratings"]

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

with open("app_data.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
