from users_database import *
from datetime import datetime


class RedisDatabase(Database):
    def __init__(self, connection_factory, database):
        self._connection = connection_factory.create_connection()
        self._database = database
    
    def _cache_user_time(self, id, time):
        self._connection.add(id, str(time))

    def upsert_user_time(self, id, time):
        self._cache_user_time(id, time)
        self._database.upsert_user_time(id, time)

    def get_user_time(self, id):
        result = self._connection.get(id)
        print(result)
        if result is None:
            print("Cache miss", id)
            result = self._database.get_user_time(id)
            if result is not None:
                self._cache_user_time(id, result)
            return result
        return datetime.strptime(result, "%Y-%m-%d %H:%M:%S.%f")

