import os
import mysql.connector
from mysql.connector import pooling

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="bobo_pool",
            pool_size=10,
            pool_reset_session=True,
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            database=os.getenv("MYSQL_DATABASE", "bobo_tour_management"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            charset="utf8mb4",
            use_unicode=True,
        )
    return _pool

def get_connection():
    return get_pool().get_connection()

def get_cursor(conn=None):
    if conn is None:
        conn = get_connection()
    return conn.cursor(dictionary=True)