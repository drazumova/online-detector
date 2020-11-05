import yaml

from db_connection import DatabaseConnection
from service_connection import FingerprintServiceConnection

class ConnectionManager:
    def __init__(self, db_config_path = 'connection/db_config.yaml', service_config_path = 'connection/service_config.yaml'):
        with open(db_config_path, 'r') as config: 
            args = yaml.load(config) # todo
            self._username = args['username']
            self._db_host = args['host']
            self._db_port = args['port']
        
        with open(service_config_path, 'r') as config:
            args = yaml.load(config) # todo
            self._service_host = args['host']
            self._service_port = args['port']


    def create_database_connection(self):
        return DatabaseConnection(self._username, self._db_host, self._db_port)
    
    def create_service_connection(self):
        return FingerprintServiceConnection(self._service_host, self._service_port)