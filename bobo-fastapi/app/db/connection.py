import os
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        database=os.getenv("MYSQL_DATABASE", "bobo_tour_management"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
    )
    return conn

def get_cursor(conn=None):
    if conn is None:
        conn = get_connection()
    return conn.cursor(dictionary=True)