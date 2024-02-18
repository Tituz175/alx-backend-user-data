#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from api.v1.auth.session_auth import SessionAuth
import uuid
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session authentication with expiration class
    """
    def __init__(self) -> None:
        super().__init__()
        duration = os.getenv("SESSION_DURATION")
        self.session_duration = 0
        if duration.isdigit():
            self.session_duration = int(duration)

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session for the given user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The session ID if successful, otherwise None.
        """
        session_id = super().create_session(user_id)
        if not session_id or not isinstance(session_id, str):
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID if found,
            otherwise None.
        """
        if not session_id:
            return None
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict.get("user_id")
            if "created_at" not in session_dict:
                return None
            time_now = datetime.now()
            set_time = timedelta(seconds=self.session_duration)
            exp_time = session_dict.get("created_at") + set_time
            if exp_time < time_now:
                return None
            else:
                return session_dict.get("user_id")
