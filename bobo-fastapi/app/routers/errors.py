"""
errors.py — Converts unexpected exceptions into safe HTTP errors.
Raw DB messages are logged server-side and never sent to the client.
"""

import logging
import mysql.connector
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def db_error(e: Exception) -> HTTPException:
    logger.exception(e)
    if isinstance(e, mysql.connector.Error):
        if e.errno == 3819:  # CHECK constraint violated
            return HTTPException(400, "Some values are out of the allowed range.")
        if e.errno == 1062:  # duplicate entry
            return HTTPException(409, "This data already exists.")
        if e.errno == 1452:  # foreign key fails
            return HTTPException(400, "Related data not found.")
    return HTTPException(500, "Something went wrong. Please try again.")

def safe_msg(e: Exception) -> str:
    """For endpoints that return {"error": ...} instead of raising."""
    logger.exception(e)
    return "Something went wrong. Please try again."