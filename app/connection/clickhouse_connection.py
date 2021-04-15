from clickhouse_driver import Client
from connection.connection_configuration import *
from connection.db_connection import *
import yaml


class ClickHouseConnection(DatabaseConnection):
    def __init__(self, host, user, password):
        self._client = Client(host, user=user, password=password)

    def execute(self, request):
        return self._client.execute(request)


class ClickHouseConnectionConfig(DatabaseConnectionConfig):
    def __init__(self, filename):
        with open(filename, 'r') as config: 
            args = yaml.load(config)
            self.host = args['host']
            self.user = args['user']
            self.password = args['password']

    def create_connection(self):
        return ClickHouseConnection(self.host, user=self.user, password=self.password)


class ClickHouseConnectionConfigurationManager(ConnectionConfigurationManager):
    @staticmethod
    def create_database_conf(filename="app/connection/conf/clickhouse_config.yaml"):
        return ClickHouseConnectionConfig(filename)
