import psycopg2
import atexit

class DatabaseHelper:
    _online_time_table = 'user_online_time'
    _username = 'postgres'    

    def __init__(self):
        self._connection = psycopg2.connect(database=self._username, user=self._username, password=self._username, host='localhost', port='5432')
        self._cursor = self._connection.cursor()
        atexit.register(self.close)

    def close(self):
        self._cursor.close()
        self._connection.close()

    def upsert_user_time(self, id, time):
        self._cursor.execute(("INSERT INTO {0}(id, last_time) VALUES({1}, timestamp '{2}')" +
        " ON CONFLICT (id) DO UPDATE SET last_time = EXCLUDED.last_time").format(self._online_time_table, id, time))
        self._connection.commit()

    def get_user_time(self, id):
        self._cursor.execute("SELECT last_time FROM {} WHERE id = {}".format(self._online_time_table, id))
        result = self._cursor.fetchall()
        if not result:
            return None
        if len(result) != 1:
            print("Error on getting select result", result)
            return None
        return result[0][0]