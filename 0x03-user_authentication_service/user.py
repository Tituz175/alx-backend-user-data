#!/usr/bin/env python3
"""
sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

Base = declarative_base()


class User(Base):
    """
    sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
