import psycopg2
import atexit
import yaml

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


class DatabaseConnectionManager:
    def __init__(self, config_path = 'db_confing.yaml'):
        config_file = open(config_path, 'r')
        args = yaml.load(config_file) # todo

        self._username = args['username']
        self._host = args['host']
        self._port = args['port']
        
        config_file.close()

    def create_connection(self):
        return DatabaseConnection(self._username, self._host, self._port)


class Database:
    _user_oline_table = 'user_online_time'

    def __init__(self, connection):
        self._connection = connection
    
    def upsert_user_time(self, id, time):
        request = ("INSERT INTO {0}(id, last_time) VALUES({1}, timestamp '{2}')" +
        " ON CONFLICT (id) DO UPDATE SET last_time = EXCLUDED.last_time").format(self._user_oline_table, id, time)
        self._connection.execute(request)
        self._connection.commit()

    def get_user_time(self, id):
        request = "SELECT last_time FROM {} WHERE id = {}".format(self._user_oline_table, id)
        self._connection.execute(request)
        result = self._connection.fetch()
        if not result:
            return None
        if len(result) != 1:
            print("Error on getting select result", result) #todo
            return None
        return result[0][0]
