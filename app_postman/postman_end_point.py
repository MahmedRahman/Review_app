from flask import request, jsonify,Blueprint
import openai


endpoint_postman_app = Blueprint('endpoint_postman_app', __name__)

# Global response variable
response = None

@endpoint_postman_app.route('/api/v1/generate', methods=['GET'])
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

@endpoint_postman_app.route('/api/v1/generate_batch', methods=['POST'])
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








# import os
# import openai
# from flask import Flask, request, jsonify
# from dotenv import load_dotenv


# load_dotenv()

# openai.api_key = os.environ["OPENAIAPIKEY"]
# app = Flask(__name__)

# # Global response variable
# response = None

# # def generate_response():
# #     data = request.get_json()

# #     try:
# #         prompt = data['prompt']
# #         list_data = data['data']
# #         if not isinstance(list_data, list):
# #             return jsonify({"error": "Expected a list of maps"}), 400

# #     except KeyError as e:
# #         return jsonify({"error": f"Missing key: {e.args[0]}"}), 400


# #     response = openai.Completion.create(
# #         engine="text-davinci-003",  # Code generation model
# #         prompt=prompt,
# #         max_tokens=150,
# #         temperature=0.7,
# #         user="my-unique-identifier"
# #     )



# #     return jsonify({"response": response.choices[0].text.strip()})



# app = Flask(__name__)

# # Global response variable
# response = None

# @app.route('/single', methods=['POST'])
# def generate_single_response():
#     global response
#     data = request.get_json()
#     try:
#         prompt = data['prompt']
#     except KeyError as e:
#         return jsonify({"error": f"Missing key: {e.args[0]}"}), 400

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150,
#         temperature=0.7,
#         user="my-unique-identifier"
#     )

#     return jsonify({"response": response.choices[0].text.strip()})

# @app.route('/multiple', methods=['POST'])
# def generate_multiple_responses():
#     global response
#     data = request.get_json()

#     if not isinstance(data, list):
#         return jsonify({"error": "Expected a list of maps"}), 400

#     responses = []
#     for item in data:
#         try:
#             api_name = item['api_name']
#             curl = item['curl']
#             prompt = item['prompt']
#         except KeyError as e:
#             return jsonify({"error": f"Missing key in item: {e.args[0]}"}), 400

#         # Use the single response function
#         single_response = generate_single_response(prompt)

#         # Append the response text to the responses list
#         responses.append({"api_name": api_name, "response": single_response})

#     # Return a JSON object with all the responses
#     return jsonify(responses)

# if __name__ == '__main__':
#     app.run(debug=True)
