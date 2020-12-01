from users_database import *

class RedisDatabase(Database):
    def __init__(self, connection_factory, database): # todo: replace with config object
        self._connection = connection_factory.create_connection()
        self._database = database
    
    def __cache_user_time(self, id, time):
        # connection = self._connection_factory.create_connection()
        self._connection.add(id, time)

    def upsert_user_time(self, id, time):
        self.__cache_user_time(id, time)
        self._database.upsert_user_time(id, time)

    def get_user_time(self, id):
        # connection = self._connection_factory.create_connection()
        result = self._connection.get(id)
        print(result)
        if not result:
            print("Cached miss", id)
            result = self._database.get_user_time(id)
            cache_user_time(self, id, time)
            return result
        return result
