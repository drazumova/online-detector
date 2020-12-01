import yaml

from db_connection import DatabaseConnection
from fingerprint_service_connection import FingerprintServiceConnection
from connection_configuration import *

class FingerpritConnectionConfigurationManager(ConnectionConfigurationManager):
    def create_database_conf(filename="connection/conf/fp_db_config.yaml"):
        return DatabaseConnectionConfig(filename)
