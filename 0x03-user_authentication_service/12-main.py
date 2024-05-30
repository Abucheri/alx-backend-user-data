#!/usr/bin/env python3
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

# Register a user
auth.register_user(email, password)

# Create a session for the user
session_id = auth.create_session(email)
print(f"Session ID: {session_id}")

# Retrieve the user using the session ID
user = auth.get_user_from_session_id(session_id)
print(f"User: {user}")

# Attempt to retrieve a user with an invalid session ID
invalid_user = auth.get_user_from_session_id("invalid_session_id")
print(f"Invalid User: {invalid_user}")
