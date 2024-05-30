#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt

    Args:
        password (str): The password to hash.

    Returns:
      str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: The string representation of the generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The registered user object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            return bcrypt.checkpw(password.encode(), hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session ID for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID if user exists, None otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User | None:
        """
        Finds a user by their session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            User: The user object corresponding to the session ID,
                  or None if not found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
