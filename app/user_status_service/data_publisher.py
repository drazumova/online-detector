import sys
sys.path.append('connection/')

from rabbit_connection import *
from rabbit_connection import RabbitConnectionConfig

import json

class DataPublisher:
    def __init__(self, out_queue = RabbitConnectionConfig.geoip_queue):
        self._out = out_queue
        self.connection_conf = RabbitConnectionConfigurationManager.create_rabbit_conf()

    def publish(self, id, data):
        connection = self.connection_conf.create_connection(self._out)
        data["Fp_Id"] = id
        connection.basic_publish(self._out, json.dumps(data))
        