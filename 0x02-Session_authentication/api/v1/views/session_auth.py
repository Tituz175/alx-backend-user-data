#!/usr/bin/env python3
""" Module of Session authentication views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """Handles user login via session authentication.

    This endpoint handles user login via session authentication.
    It expects a POST request with email and password parameters.
    It verifies the provided credentials, creates a session for the user
    if authentication is successful, and sets a session cookie.

    Returns:
        str: JSON response indicating the user's login status or
        any errors encountered.
    """
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    user = users[0].to_json()
    from api.v1.app import auth
    session_id = auth.create_session(user.get("id"))
    session_env = os.getenv("SESSION_NAME")
    response = jsonify(user)
    response.set_cookie(session_env, session_id)
    return response
