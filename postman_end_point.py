import os
import openai
from flask import request, jsonify
from dotenv import load_dotenv


load_dotenv()
openai.api_key = "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"

def generate_response():
    data = request.get_json()

    try:
        prompt = data['prompt']
    except KeyError as e:
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400


    response = openai.Completion.create(
        engine="text-davinci-003",  # Code generation model
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        user="my-unique-identifier"
    )



    return jsonify({"response": response.choices[0].text.strip()})
