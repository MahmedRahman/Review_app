from flask import jsonify

def create_response(data=None, success=True, code=200, errors=None):
    response = {
        "success": success,
        "code": code
    }
    if data is not None:
        response["data"] = data
    if errors is not None:
        response["errors"] = errors

    return jsonify(response), code
