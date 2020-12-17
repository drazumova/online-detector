import requests
import json

import json
import sys
sys.path.append('connection/')

from rabbit_connection import *


class GEOIpBlock:
    _service_url = 'http://ip-api.com/json/'
    _fields = ['timezone', 'countryCode', 'country']

    def __init__(self, in_queue = RabbitConnectionConfig.geoip_queue,
        out_queue=RabbitConnectionConfig.storing_queue):
        self._in = in_queue
        self._out = out_queue
        self._conf = RabbitConnectionConfigurationManager.create_rabbit_conf()

    def post(self, data):
        print("geoip pusblish", data)
        connection = self._conf.create_connection(self._out)
        connection.basic_publish(self._out, data)

    def get(self, ch, method, properties, body):
        print("geoip get data", body)
        key = 'X-Real-Ip'
        data = json.loads(body)
        info = self.get_data(data[key])
        # if info is None:
        #     self.post(str(data))    
        #     return
        for field in self._fields:
            if field in info.keys():
                data[field] = info[field]
        self.post(str(data))

    def get_data(self, ip):
        session = requests.Session()
        response = session.get(self._service_url + ip)
        print(response)
        data = json.loads(response.text)
        if data['status'] != 'success':
            return {}
        return data

    def start(self):
        connection = self._conf.create_connection(self._in)
        connection.start_consuming(self._in, self.get)

if __name__== '__main__':
    block = GEOIpBlock()
    block.start()
