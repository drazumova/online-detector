from users_db import *

class RedisDatabase(Database):
    def __init__(self, create_connection, database):
        self._create_connection = create_connection
        self._database = database
    
    def cache_user_time(self, id, time):
        connection = self._create_connection()
        connection.add(id, time)

    def upsert_user_time(self, id, time):
        self.cache_user_time(id, time)
        self._database.upsert_user_time(id, time)

    def get_user_time(self, id):
        connection = self._create_connection()
        result = connection.get(id)
        print(result)
        if not result:
            result = self._database.get_user_time(id)
            cache_user_time(self, id, time)
            return result
        return result

    