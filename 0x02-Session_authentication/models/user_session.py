#!/usr/bin/env python3
"""
user session module
"""

from models.base import Base


class UserSession(Base):
    """
    UserSession class representing sessions stored in the database
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a new UserSession instance.

        Args:
            user_id (str): The ID of the user associated with the session.
            session_id (str): The session ID.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
