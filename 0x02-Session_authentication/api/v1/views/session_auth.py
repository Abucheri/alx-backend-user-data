#!/usr/bin/env python3
"""
Session Authentication view for API
"""

import os
from flask import request, jsonify, abort
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /api/v1/auth_session/login
    Handles login and session creation
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    # Check for missing email
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    # Check for missing password
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    # Find the User by email
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate the password
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a Session ID for the User
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())

    session_name = os.getenv('SESSION_NAME')
    # Set the session ID cookie
    response.set_cookie(session_name, session_id)

    return response
