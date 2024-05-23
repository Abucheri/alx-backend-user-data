#!/usr/bin/env python3
"""
SessionAuth module
"""

import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class for handling session authentication.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id and stores it in
        user_id_by_session_id.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The created Session ID, or None if user_id is
                 None or not a string.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID using uuid.uuid4()
        session_id = str(uuid.uuid4())

        # Store the session ID and user ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the User ID based on the Session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The User ID associated with the session ID,
                 or None if session_id is None or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Use .get() to retrieve the user ID associated with the session ID
        # and return None if the session ID is not found
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            User: The User instance associated with the session ID,
                  or None if no user is found.
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # Retrieve the User instance from the database using the user ID
        return User.get(user_id)
