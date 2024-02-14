#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic authentication class
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
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
