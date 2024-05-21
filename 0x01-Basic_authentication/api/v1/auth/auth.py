#!/usr/bin/env python3
"""
Auth module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class for managing API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that
                                        do not require authentication.

        Returns:
            bool: False for now, indicating no path requires authentication.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path ends with a slash for consistency
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            # Ensure excluded path ends with a slash for consistency
            if excluded_path[-1] != '/':
                excluded_path += '/'

            # Handle wildcard matching
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
            str: None for now, indicating no Authorization header is provided.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user from the request.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
            TypeVar('User'): None for now, indicating
                             no current user is retrieved.
        """
        return None
