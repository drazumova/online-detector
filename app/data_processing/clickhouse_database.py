import sys
sys.path.append('connection/')

from connection_configuration import *


class ClickHouseDatabase:
    _table = "storage"
    _fignerprint_id = "Fingerprint-ID"
    fileds_list = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr'] # from fingerprint counter
     
    def __init__(self, connection_factory):
        self._connection_factory = connection_factory  
        self.init_table() 
    
    def init_table(self):
        connection = self._connection_factory.create_connection()
        columns = "{} long, {}".format(self._fignerprint_id, " ".join(map(lambda x: x + " str", self._fields_list)))
        request = ("CREATE TABLE IF NOT EXISTS {} ({})").format(self._table, columns)
        connection.execute(request)
        connection.commit()
    
    def store(self, fingerprint_id, fileds):
        connection = self._connection_factory.create_connection()
        request = "INSERT INTO {}((*) VALUES({}, {})".format(self._table, fingerprint_id, ", ".join(fileds))
        connection.execute(request)
