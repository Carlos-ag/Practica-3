# BiciMadAPI/app/models/db.py
import mysql.connector
from mysql.connector import Error
from app.config import DB_CONFIG

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection
