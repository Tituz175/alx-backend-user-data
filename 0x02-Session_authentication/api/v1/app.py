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


@app.before_request
def before_request():
    """
    _summary_

    Returns:
        str: _description_
    """
    if auth:
        excluded_paths = ['/api/v1/status/',
                          '/api/v1/unauthorized/', '/api/v1/forbidden/']
        if auth.require_auth(request.path, excluded_paths):
            if not (auth.authorization_header(request)):
                abort(401, description="Unauthorized")
            if not (auth.current_user(request)):
                abort(403, description="Forbidden")
            else:
                request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
