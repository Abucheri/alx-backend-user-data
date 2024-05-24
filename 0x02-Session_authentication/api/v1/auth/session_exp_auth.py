#!/usr/bin/env python3
"""
Session expiration chscker module
"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for handling session authentication with expiration.
    """

    def __init__(self):
        """
        Constructor method.

        Assigns an instance attribute session_duration based on the
        environment variable SESSION_DURATION, casting it to an integer.
        If the environment variable doesn’t exist or can’t be parsed
        to an integer, assigns 0 to session_duration.
        """
        super().__init__()
        session_duration_str = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration_str)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID by calling super().
        Returns None if super() fails to create a Session ID.
        Stores session data in the user_id_by_session_id dictionary
        with an additional 'session dictionary' containing user_id and
        creation time. Returns the created Session ID.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The created Session ID, or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        if user_id is None:
            return None

        # Create a session dictionary with user ID and creation time
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID based on the Session ID with session expiration.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The User ID associated with the session ID,
                 or None if session_id is None, not found, or expired.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        user_id = session_dict.get('user_id')
        created_at = session_dict.get('created_at')

        # Check if session has expired based on session_duration
        if self.session_duration <= 0:
            return user_id

        if created_at is None:
            return None

        expire_time = created_at + timedelta(seconds=self.session_duration)
        if expire_time < datetime.now():
            return None

        return user_id
