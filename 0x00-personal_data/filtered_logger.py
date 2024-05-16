#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import logging
import re
from typing import List
from os import environ
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all
                   fields in the log line (message).
    Returns:
        str: A string with specified fields obfuscated
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        NotImplementedError

        Formats the log record by redacting specified fields.

        Args:
            record: The LogRecord to be formatted.

        Returns:
            str: The formatted log record.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


# Define the fields from user_data.csv that are considered PII
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger object.

    Returns:
        Logger: A configured logger object.
    """
    # Create a logger named "user_data"
    logger = logging.getLogger("user_data")

    # Set the logging level to INFO
    logger.setLevel(logging.INFO)

    # Prevent messages from being propagated to other loggers
    logger.propagate = False

    # Create a StreamHandler to log to the console
    stream_handler = logging.StreamHandler()

    # Create a RedactingFormatter with PII_FIELDS
    formatter = RedactingFormatter(PII_FIELDS)

    # Set the formatter for the StreamHandler
    stream_handler.setFormatter(formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""

    # Get database credentials from environment variables
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    # Connect to the database
    db = mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return db


def main() -> None:
    """Main function to retrieve and log filtered user data."""
    # Get a logger
    logger = get_logger()

    # Get a database connection
    db = get_db()

    # Create a cursor to execute queries
    cursor = db.cursor()

    # Execute a query to retrieve all rows from the users table
    cursor.execute("SELECT * FROM users")

    # Fetch all rows
    rows = cursor.fetchall()

    # Log each row in a filtered format
    for row in rows:
        filtered_row = {}
        for field, value in zip(cursor.column_names, row):
            if field in PII_FIELDS:
                filtered_row[field] = "***"
            else:
                filtered_row[field] = value
        # Convert the filtered_row dictionary to a formatted string
        log_message = ("; ".join([f"{key}={value}" for key,
                       value in filtered_row.items()]))
        log_message += ";"  # Append a semicolon at the end
        logger.info(log_message)

    # Close the cursor and database connection
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
