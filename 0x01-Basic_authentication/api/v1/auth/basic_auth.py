#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic authentication class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        _summary_

        Returns:
            str: _description_
        """
        if authorization_header is None \
                or not (isinstance(authorization_header, str)) \
                or "Basic " not in authorization_header:
            return None

        return authorization_header.split(" ")[-1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        _summary_

        Returns:
            str: _description_
        """
        if base64_authorization_header and \
                isinstance(base64_authorization_header, str):
            try:
                return base64.b64decode(base64_authorization_header)\
                    .decode()
            except Exception:
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        _summary_

        Returns:
            str: _description_
        """
        if decoded_base64_authorization_header and \
                isinstance(decoded_base64_authorization_header, str) and\
                ":" in decoded_base64_authorization_header:
            return tuple(
                decoded_base64_authorization_header.split(":")
            )
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        _summary_

        Returns:
            str: _description_
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if users == [] or not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        _summary_

        Returns:
            str: _description_
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            user_token = self.extract_base64_authorization_header(auth_header)
            if user_token:
                decoded_token = self.decode_base64_authorization_header(
                    user_token)
                if decoded_token:
                    email, password = self.extract_user_credentials(
                        decoded_token)
                    if email:
                        return self.user_object_from_credentials(
                            email, password)
        return
