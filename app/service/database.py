from users_db import *
from redis_db import *

import sys
sys.path.append('connection/')

from connection import *

class DatabaseFactory:
    def create_pg_database():
        pg_config = ConnectionConfigurationManager.create_database_conf
        return Database(pg_config.create_connection)

    def create_caching():
        redis_config = RedisConnectionConfigurationManager.create_database_conf
        pg_database = create_pg_database()
        return RedisDatabase(redis_config.create_connection, pg_database)

    def create_default():
        return create_caching()
        