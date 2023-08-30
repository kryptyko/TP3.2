import mysql.connector

class DatabaseConnectionproduction:
    _connection = None
    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = mysql.connector.connect(
                host = '172.17.0.4',
                user = 'root',
                port = '3306',
                password = '1127As305001.',
                database = 'production'
            )
        return cls._connection
    
    @classmethod
    def execute_query(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        cls._connection.commit()
        return cursor
     
    @classmethod
    def fetch_one(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    
    @classmethod
    def fetch_all(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None