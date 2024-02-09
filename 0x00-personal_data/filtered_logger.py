#!/usr/bin/env python3
"""
A function called filter_datum that returns the log message obfuscated.
This function uses a regex to replace occurrences of certain field values.


Keyword arguments:
fields -- a list of strings representing all fields to obfuscate
redaction -- a string representing by what the field will be obfuscated
message -- a string representing the log line
separator -- a string representing by which character is separating all
fields in the log line (message)
Return: none
"""

from typing import List
import re
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function documentation"""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return (message)


def get_logger() -> logging.Logger:
    """Function documentation"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """Fuction documentation"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connect(user=db_username,
                                         password=db_password,
                                         host=db_host,
                                         database=db_name)
    return connection


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Function documentation"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Function documentation"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
