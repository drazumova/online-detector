import sys
sys.path.append('connection/')

from connection_configuration import *
from geoip_block import *

from logger import Logger


class ClickHouseDatabase:
    _table = "storage"
    _fignerprint_id = "Fingerprint_ID"
    _fields_list = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr', 'X-Real-Ip']
     
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory  
        self.init_table() 
    
    def init_table(self):
        connection = self._connection_factory.create_connection()
        # connection.execute("drop table {}".format(self._table))
        columns = "{} UInt64, {}".format(self._fignerprint_id, ", ".join(map(lambda x: x + " String", self._fields_list)))
        request = ("CREATE TABLE IF NOT EXISTS {} ({}) ENGINE = MergeTree() ORDER BY {}").format(self._table, columns.replace("-", "_"), self._fignerprint_id)
        Logger.log(request)
        connection.execute(request)
    
    def store(self, fingerprint_id, data):
        allowed_keys = self._fields_list + GEOIpBlock._fields
        keys = [key for key in data.keys() if key in allowed_keys]
        fields = [data[key] for key in keys]
        connection = self._connection_factory.create_connection()
        column_list = self._fignerprint_id + ", " + ", ".join(keys).replace("-", "_")
        value_list =  ", ".join(map(lambda x: "'" + x + "'", fields))
        request = "INSERT INTO {}({}) VALUES ({}, {})".format(self._table, column_list, fingerprint_id, value_list)
        Logger.log(request)
        connection.execute(request)
