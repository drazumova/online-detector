from redis_database import *
from connection.redis_connection import *
from connection.connection_configuration import *


class DatabaseFactory:
    @staticmethod
    def create_pg_database():
        pg_config = ConnectionConfigurationManager.create_database_conf()
        return Database(pg_config)

    @staticmethod
    def create_caching():
        redis_config = RedisConnectionConfigurationManager.create_database_conf()
        pg_database = DatabaseFactory.create_pg_database()
        return RedisDatabase(redis_config, pg_database)

    @staticmethod
    def create_default():
        return DatabaseFactory.create_caching()
