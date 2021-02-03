import requests
import json

import json
import sys
sys.path.append('connection/')

from rabbit_connection import *
from logger import Logger

class GEOIpBlock:
    _service_url = 'http://ip-api.com/json/'
    _fields = ['timezone', 'countryCode', 'country', 'city', 'regionName']

    def __init__(self, in_queue = RabbitConnectionConfig.geoip_queue,
        out_queue=RabbitConnectionConfig.storing_queue):
        self._in = in_queue
        self._out = out_queue
        self._conf = RabbitConnectionConfigurationManager.create_rabbit_conf()

    def post(self, data):
        Logger.log("geoip publish " + str(data))
        connection = self._conf.create_connection(self._out)
        connection.basic_publish(self._out, data)

    def get(self, ch, method, properties, body):
        data = json.loads(body)
        key = 'X-Real-Ip'
        if 'X-Test-Ip' in data.keys():
            key = 'X-Test-Ip'
        Logger.log("geoip get data " + str(data))
        info = self.get_data(data[key])
        fp_id = data["Fp_Id"]
        for field in self._fields:
            if field in info.keys():
                data[field] = info[field]
        self.post(json.dumps(data))

    def get_data(self, ip):
        session = requests.Session()
        response = session.get(self._service_url + ip)
        Logger.log("geoip response " + str(response.text))
        data = json.loads(response.text)
        if data['status'] != 'success':
            return {}
        return data

    def start(self):
        connection = self._conf.create_connection(self._in)
        connection.start_consuming(self._in, self.get)

if __name__== '__main__':
    Logger.log("start geoip block")
    block = GEOIpBlock()
    block.start()
