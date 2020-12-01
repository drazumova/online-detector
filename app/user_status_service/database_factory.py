from users_database import *
from redis_database import *
from redis_connection import *

import sys
sys.path.append('connection/')

from connection_configuration import *

class DatabaseFactory:
    def create_pg_database():
        pg_config = ConnectionConfigurationManager.create_database_conf()
        return Database(pg_config)

    def create_caching():
        redis_config = RedisConnectionConfigurationManager.create_database_conf()
        pg_database = DatabaseFactory.create_pg_database()
        return RedisDatabase(redis_config, pg_database)

    def create_default():
        return DatabaseFactory.create_caching()
