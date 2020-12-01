import yaml

from db_connection import DatabaseConnection
from fingerprint_service_connection import FingerprintServiceConnection

class ConnectionConfigurationManager:
    def create_service_conf(filename="connection/conf/fingerprint_service_config.yaml"):
        return ServiceConnectionConfig(filename)
        
    def create_database_conf(filename="connection/conf/service_db_config.yaml"):
        return DatabaseConnectionConfig(filename)
    

class ConnectionConfig:
    def __init__(self, filename):
        with open(filename, 'r') as config: 
            args = yaml.load(config) # todo
            self.host = args['host']
            self.port = args['port']

    def create_connection(self):
        pass


class DatabaseConnectionConfig(ConnectionConfig):
    def __init__(self, filename):
        super(DatabaseConnectionConfig, self).__init__(filename)
        with open(filename, 'r') as config: 
            args = yaml.load(config) # todo
            print(args)
            self.username = args['username']

    def create_connection(self):
        return DatabaseConnection(self.username, self.host, self.port)

class ServiceConnectionConfig(ConnectionConfig):
    def __init__(self, filename):
        super(ServiceConnectionConfig, self).__init__(filename)

    def create_connection(self):
        return FingerprintServiceConnection(self.host, self.port)
        