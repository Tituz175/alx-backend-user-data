#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    The authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): A list of paths that are excluded
            from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if not path or not excluded_paths:
            return True

        path = path if path[-1] == "/" else f"{path}/"
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The request object.

        Returns:
            str: The value of the Authorization header if present,
            otherwise None.
        """
        if request is None:
            return None

        header = request.headers.get("Authorization")
        if header:
            return header

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.

        Args:
            request: The request object.

        Returns:
            User: The current user object.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.

        Args:
            request: The request object.

        Returns:
            str: The value of the session cookie if present, otherwise None.
        """
        if not request:
            return None
        section_val = os.getenv("SESSION_NAME")
        return request.cookies.get(section_val)
