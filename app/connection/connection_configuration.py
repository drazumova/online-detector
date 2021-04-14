import yaml

from connection.db_connection import DatabaseConnection
from connection.fingerprint_service_connection import FingerprintServiceConnection


class ConnectionConfigurationManager:
    @staticmethod
    def create_service_conf(filename="app/connection/conf/fingerprint_service_config.yaml"):
        return ServiceConnectionConfig(filename)

    @staticmethod
    def create_database_conf(filename="app/connection/conf/service_db_config.yaml"):
        return DatabaseConnectionConfig(filename)
    

class ConnectionConfig:
    def __init__(self, filename):
        with open(filename, 'r') as config: 
            args = yaml.load(config)
            self.host = args['host']
            self.port = args['port']

    def create_connection(self):
        pass


class DatabaseConnectionConfig(ConnectionConfig):
    def __init__(self, filename):
        super(DatabaseConnectionConfig, self).__init__(filename)
        with open(filename, 'r') as config: 
            args = yaml.load(config)
            print(args)
            self.username = args['username']

    def create_connection(self):
        return DatabaseConnection(self.username, self.host, self.port)


class ServiceConnectionConfig(ConnectionConfig):
    def __init__(self, filename):
        super(ServiceConnectionConfig, self).__init__(filename)

    def create_connection(self):
        return FingerprintServiceConnection(self.host, self.port)
