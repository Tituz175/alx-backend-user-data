#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
env_val = os.getenv("AUTH_TYPE")

if env_val == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif env_val == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif env_val == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif env_val == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()



@app.before_request
def before_request():
    """
    Executes before each request.

    Checks authentication for each request based on the authentication
    type set in the environment variable.
    If authentication is required for the requested path, it verifies
    the presence of either an Authorization header or a session cookie.
    If authentication is successful, it attaches the current user to
    the request object.

    Returns:
        None
    """
    if auth:
        excluded_paths = ['/api/v1/status/', '/api/v1/auth_session/login/',
                          '/api/v1/unauthorized/', '/api/v1/forbidden/']
        if auth.require_auth(request.path, excluded_paths):
            if not (auth.authorization_header(request)) and\
                    not (auth.session_cookie(request)):
                abort(401, description="Unauthorized")
            if not (auth.current_user(request)):
                abort(403, description="Forbidden")
            else:
                request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles 404 errors.

    Returns:
        str: JSON response indicating the error.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles 401 errors.

    Returns:
        str: JSON response indicating the error.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles 403 errors.

    Returns:
        str: JSON response indicating the error.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
