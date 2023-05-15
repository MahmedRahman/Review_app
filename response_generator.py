from flask import request, jsonify
import openai

# Global response variable
response = None

def generate_single_response():
    global response
    data = request.get_json()
    try:
        prompt = data['prompt']
    except KeyError as e:
        return jsonify({"error": f"Missing key: {e.args[0]}"}), 400

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        user="my-unique-identifier"
    )

    return jsonify({"response": response.choices[0].text.strip()})

def generate_multiple_responses():
    global response
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of maps"}), 400

    responses = []
    for item in data:
        try:
            api_name = item['api_name']
            curl = item['curl']
            prompt = item['prompt']
        except KeyError as e:
            return jsonify({"error": f"Missing key in item: {e.args[0]}"}), 400

        # Use the single response function
        single_response = generate_single_response()

        # Append the response text to the responses list
        responses.append({"api_name": api_name, "response": single_response})

    # Return a JSON object with all the responses
    return jsonify(responses)
