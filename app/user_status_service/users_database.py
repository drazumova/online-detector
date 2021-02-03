import sys
sys.path.append('connection/')

from connection_configuration import *

class Database: # rename
    _user_oline_table = 'user_online_time'
    _id = 'id'
    _time = 'last_time'

    def __init__(self, connection_factory):
        self._connection_factory = connection_factory  
        self.init_table()

    def init_table(self):
        connection = self._connection_factory.create_connection()
        request = ("CREATE TABLE IF NOT EXISTS {} ({} int UNIQUE, {} timestamp)").format(self._user_oline_table, self._id, self._time)
        connection.execute(request)
        connection.commit()
        connection.close()
    
    def upsert_user_time(self, id, time):
        connection = self._connection_factory.create_connection()
        request = ("INSERT INTO {0}({4}, {3}) VALUES({1}, timestamp '{2}')" +
        " ON CONFLICT ({4}) DO UPDATE SET {3} = EXCLUDED.{3};").format(self._user_oline_table, id, time, self._time, self._id)
        connection.execute(request)
        connection.commit()
        connection.close()

    def get_user_time(self, id):
        connection = self._connection_factory.create_connection()
        request = "SELECT last_time FROM {} WHERE id = {};".format(self._user_oline_table, id)
        connection.execute(request)
        result = connection.fetch()
        connection.close()
        if not result:
            return None
        if len(result) != 1:
            print("Error on getting select result", result) #todo
            return None
        return result[0][0]
