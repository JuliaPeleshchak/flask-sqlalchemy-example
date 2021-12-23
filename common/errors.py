from flask import jsonify


def bad_request(message):
    response = jsonify({"error": "Bad request", "message": message})
    response.status_code = 400
    return response


def forbidden(message):
    response = jsonify({"error": "Forbidden", "message": message})
    response.status_code = 403
    return response


def not_found(message):
    response = jsonify({"error": "Not Found", "message": message})
    response.status_code = 404
    return response
