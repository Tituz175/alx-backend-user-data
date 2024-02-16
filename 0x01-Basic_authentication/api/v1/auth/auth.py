#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from flask import request
from typing import List, TypeVar
import re


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

        for link in excluded_paths:
            if link.startswith(path):
                return False
            elif link[-1] == "*":
                if path.startswith(link[:-1]):
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
