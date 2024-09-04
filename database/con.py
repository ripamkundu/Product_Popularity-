import mysql.connector
from mysql.connector import errorcode
from database.settings import (
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_DB,
    MYSQL_PORT,
)
from fastapi import HTTPException


db_config = {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "host": MYSQL_HOST,
    "port": MYSQL_PORT,
    "database": MYSQL_DB,
    "raise_on_warnings": True,
}


def connect():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise HTTPException(
                status_code=500, detail="Error: Access denied. Check your credentials."
            )
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise HTTPException(
                status_code=500, detail="Error: The specified database does not exist."
            )
        else:
            raise HTTPException(status_code=500, detail=f"Error: {err}")
