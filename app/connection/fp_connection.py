from connection.connection_configuration import *


class FingerprintConnectionConfigurationManager(ConnectionConfigurationManager):
    @staticmethod
    def create_database_conf(filename="app/connection/conf/fp_db_config.yaml"):
        return DatabaseConnectionConfig(filename)
