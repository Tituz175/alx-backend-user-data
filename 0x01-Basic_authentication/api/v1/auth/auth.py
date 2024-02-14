#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """The authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        _summary_

        Returns:
            str: _description_
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        _summary_

        Returns:
            str: _description_
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        _summary_

        Returns:
            str: _description_
        """
        return None
