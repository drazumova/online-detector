import sys
sys.path.append('connection/')

from connection import *

class Database:
    _user_oline_table = 'user_online_time'
    _id = 'id'
    _time = 'last_time'

    def __init__(self, connection):
        self._connection = connection
        self.init_table()

    def init_table(self):
        request = ("CREATE TABLE IF NOT EXISTS {} ({} int UNIQUE, {} timestamp)").format(self._user_oline_table, self._id, self._time)
        self._connection.execute(request)
        self._connection.commit()
    
    def upsert_user_time(self, id, time):
        request = ("INSERT INTO {0}({4}, {3}) VALUES({1}, timestamp '{2}')" +
        " ON CONFLICT ({4}) DO UPDATE SET {3} = EXCLUDED.{3};").format(self._user_oline_table, id, time, self._time, self._id)
        self._connection.execute(request)
        self._connection.commit()

    def get_user_time(self, id):
        request = "SELECT last_time FROM {} WHERE id = {};".format(self._user_oline_table, id)
        self._connection.execute(request)
        result = self._connection.fetch()
        if not result:
            return None
        if len(result) != 1:
            print("Error on getting select result", result) #todo
            return None
        return result[0][0]
