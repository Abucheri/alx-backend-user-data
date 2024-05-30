#!/usr/bin/env python3
"""
Test script for Auth module
"""

from auth import Auth
from db import DB
from sqlalchemy.exc import IntegrityError
from user import User


def main():
    auth = Auth()

    # Test 1: Register a new user
    email = "testuser@example.com"
    password = "TestPassword123"
    print(f"Registering user {email}...")
    try:
        user = auth.register_user(email, password)
        print(f"User {user.email} registered successfully with id {user.id}.")
    except IntegrityError:
        print(f"User {email} already exists.")

    # Test 2: Request a reset password token for the registered user
    print(f"Requesting reset password token for {email}...")
    try:
        token = auth.get_reset_password_token(email)
        print(f"Reset password token for {email}: {token}")
    except ValueError as e:
        print(f"Error: {e}")

    # Test 3: Attempt to request a reset password token for a non-existent user
    non_existent_email = "nonexistent@example.com"
    print(f"Requesting reset password token for {non_existent_email}...")
    try:
        token = auth.get_reset_password_token(non_existent_email)
        print(f"Reset password token for {non_existent_email}: {token}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
