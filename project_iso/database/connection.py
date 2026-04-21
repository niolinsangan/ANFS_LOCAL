"""
MySQL Database Connection Module
"""
import mysql.connector
from mysql.connector import Error
import config


class DatabaseConnection:
    """Singleton database connection handler"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish database connection"""
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(
                    host=config.DB_CONFIG['host'],
                    port=config.DB_CONFIG['port'],
                    user=config.DB_CONFIG['user'],
                    password=config.DB_CONFIG['password'],
                    database=config.DB_CONFIG['database']
                )
            return self._connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def get_connection(self):
        """Get the current connection"""
        if self._connection is None or not self._connection.is_connected():
            return self.connect()
        return self._connection
    
    def close(self):
        """Close database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("MySQL connection closed")


def get_db_connection():
    """Helper function to get database connection"""
    db = DatabaseConnection()
    return db.get_connection()


def execute_query(query, params=None, fetch=False):
    """Execute a query and optionally fetch results"""
    connection = get_db_connection()
    if connection is None:
        return None
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.lastrowid
        
        return result
    except Error as e:
        print(f"Database error: {e}")
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()


def execute_many(query, data_list):
    """Execute a query for multiple rows"""
    connection = get_db_connection()
    if connection is None:
        return False
    
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.executemany(query, data_list)
        connection.commit()
        return True
    except Error as e:
        print(f"Database error: {e}")
        connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

