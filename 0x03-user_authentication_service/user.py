#!/usr/bin/env python3
"""
This module contains the User model for the database table named 'users'.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    User model representing the 'users' table in the database.

    Attributes:
        id (int): The primary key for the user.
        email (str): The email address of the user. Non-nullable.
        hashed_password (str): The hashed password of the user. Non-nullable.
        session_id (str): The session ID for the user's current session.
                          Nullable.
        reset_token (str): The token used for resetting the user's password.
                           Nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
