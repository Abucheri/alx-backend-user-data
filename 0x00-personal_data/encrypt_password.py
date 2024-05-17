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
