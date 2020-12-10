import sys
sys.path.append('connection/')

from rabbit_connection import *

class DataPublisher:
    def __init__(self):
        self.connection_conf = RabbitConnectionConfigurationManager.create_rabbit_conf()

    def publish(self, id, data):
        connection = self.connection_conf.create_connection()
        connection.basic_publish(RabbitConnectionConfig.storing_queue, {id: data})
        