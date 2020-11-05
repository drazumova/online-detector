import psycopg2
import atexit

class DatabaseConnection:
    def __init__(self, username, host, port):
        self._connection = psycopg2.connect(database=username, user=username, password=username, host=host, port=port)
        self._cursor = self._connection.cursor()
        atexit.register(self.close)

    def close(self):
        self._cursor.close()
        self._connection.close()
    
    def execute(self, request):
        self._cursor.execute(request)

    def fetch(self):
        return self._cursor.fetchall()

    def commit(self):
        self._connection.commit()