#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from api.v1.auth.auth import Auth
import base64


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
