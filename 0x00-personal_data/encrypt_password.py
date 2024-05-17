#!/usr/bin/env python3
"""
Encrypt Password Module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        bytes: A salted, hashed password.
    """
    # Convert the password string to bytes
    password_bytes = password.encode()

    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates the input password against a hashed password.

    Args:
        hashed_password: A byte string representing the hashed password.
        password: A string representing the password to be validated.

    Returns:
        bool: True if the password matches the hashed password,
              False otherwise.
    """
    # Convert the password string to bytes
    password_bytes = password.encode()

    # Check if the password matches the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password)
