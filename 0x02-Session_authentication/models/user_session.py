#!/usr/bin/env python3
""" Sessions in database module
"""
import hashlib
from models.base import Base


class UserSession(Base):
    """
    sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
