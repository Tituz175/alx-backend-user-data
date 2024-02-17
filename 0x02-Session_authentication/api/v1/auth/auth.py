#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """The authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        _summary_

        Returns:
            str: _description_
        """
        if not (path) or not (excluded_paths):
            return True

        path = path if path[-1] == "/" else F"{path}/"
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        _summary_

        Returns:
            str: _description_
        """
        if request is None:
            return None

        header = request.headers.get("Authorization")
        if header:
            return header

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        _summary_

        Returns:
            str: _description_
        """
        return None

    def session_cookie(self, request=None):
        """
        _summary_

        Returns:
            str: _description_
        """
        if not request:
            return None
        section_val = os.getenv("SESSION_NAME")
        return request.cookies.get(section_val)
