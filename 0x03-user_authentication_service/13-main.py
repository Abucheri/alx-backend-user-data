#!/usr/bin/env python3
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

# Register a user
user = auth.register_user(email, password)
user_id = user.id

# Create a session for the user
session_id = auth.create_session(email)
print(f"Session ID: {session_id}")

# Destroy the session for the user
auth.destroy_session(user_id)

# Try to retrieve the user using the old session ID (should return None)
user = auth.get_user_from_session_id(session_id)
print(f"User after destroying session: {user}")
