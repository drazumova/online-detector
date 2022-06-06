import logging

from users_database import *
from datetime import datetime


class RedisDatabase(Database):
    def __init__(self, connection_factory, database):
        self._connection = connection_factory.create_connection()
        self._database = database
    
    def _cache_user_time(self, id, time, name):
        print("trying to save", [str(time), name])
        self._connection.add(id, [str(time), name])

    def upsert_user(self, id, time, name):
        self._cache_user_time(id, time, name)
        self._database.upsert_user(id, time, name)

    def get_user_time(self, id):
        result = self._connection.get(id)
        logging.info("redis db result", result)
        if result is None:
            logging.info("Cache miss", id)
            result = self._database.get_user_time(id)
            if result is not None:
                name = self._database.get_username(id)
                self._cache_user_time(id, result, name)
            return result
        return datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")

    def get_username(self, id):
        result = self._connection.get(id)
        logging.info("redis db result", result)
        if result is None:
            logging.info("Cache miss", id)
            result = self._database.get_username(id)
            if result is not None:
                time = self._database.get_user_time(id)
                self._cache_user_time(id, time, result)
            return result
        return result[1]


