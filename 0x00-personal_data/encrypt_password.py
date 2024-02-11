#!/usr/bin/env python3
"""
Implement a hash_password function that expects one string
argument name password and returns a salted, hashed password,
which is a byte string.
Use the bcrypt package to perform the hashing (with hashpw).
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Function documentation"""
    password_bytes = password.encode()

    salt = bcrypt.gensalt()

    hash_password = bcrypt.hashpw(password_bytes, salt)

    return hash_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Function documentation"""
    password_bytes = password.encode()

    return bcrypt.checkpw(password_bytes, hashed_password)
