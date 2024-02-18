#!/usr/bin/env python3
"""
This module manages the API authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
from models.user import User
import os
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Session authentication class with expiration and storage functionality.
    """

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
        kwargs = {
            "user_id": user_id,
            "session_id": session_id
        }
        user_session = UserSession(**kwargs)
        user_session.save()
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
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        time_now = datetime.now()
        set_time = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + set_time
        if exp_time < time_now:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """
        sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
