from connection.connection_configuration import *
from connection.db_connection import *
from rediscluster import RedisCluster
import yaml


class RedisConnection(DatabaseConnection):
    time_to_expire_s = 60

    def __init__(self, host, port, db):
        start_up = [{"host": host, "port": port}]
        self._connection = RedisCluster(startup_nodes=start_up, decode_responses=True)
        # atexit.register(self.close)

    def close(self):
        self._connection.exit()

    def add(self, key, value):
        self._connection.set(key, value, ex=self.time_to_expire_s)

    def get(self, key):
        return self._connection.get(key)


class RedisConnectionConfig(DatabaseConnectionConfig):
    def __init__(self, filename):
        super(RedisConnectionConfig, self).__init__(filename)
        with open(filename, 'r') as config:
            args = yaml.load(config)
            self.database = args['database']

    def create_connection(self):
        return RedisConnection(self.host, self.port, self.database)


class RedisConnectionConfigurationManager(ConnectionConfigurationManager):
    @staticmethod
    def create_database_conf(filename="app/connection/conf/redis_config.yaml"):
        return RedisConnectionConfig(filename)
