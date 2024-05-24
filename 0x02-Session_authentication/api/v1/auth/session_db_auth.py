#!/usr/bin/env python3
"""
SessionDB module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for handling session authentication with
    session IDs stored in the database.
    """

    def create_session(self, user_id=None):
        """
        Creates and stores a new instance of UserSession in the database.

        Args:
            user_id (str): The ID of the user associated with the session.

        Returns:
            str: The session ID.
        """
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(**{'user_id': user_id,
                                   'session_id': session_id})
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID associated with the session ID
        by querying the database.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The User ID associated with the session ID,
                 or None if not found.
        """
        if session_id is None:
            return None

        UserSession.load_from_file()

        session_ids = UserSession.search({'session_id': session_id})
        if not session_ids:
            return None

        if datetime.utcnow() > session_ids[0].created_at + timedelta(
                seconds=self.session_duration
        ):
            return None

        return session_ids[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the
        Session ID from the request cookie.

        Args:
            request: The request object. Defaults to None.

        Returns:
            bool: True if session was destroyed successfully, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        session_ids = UserSession.search({'session_id': session_id})
        if not session_ids:
            return False

        try:
            session_ids[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
