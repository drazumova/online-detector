import sys
sys.path.append('connection/')

from connection_configuration import *
from fp_connection import *

class Database:
    _fingerprint_table = 'fingerprints'
    _id = 'id'
    _fingerprint = 'fingerprint'
    _params = [] # saved parameters for fingerprint counting

    def __init__(self, connection_factory):
        self._connection_factory = connection_factory
        self.init_table()

    def init_table(self):
        connection = self._connection_factory.create_connection()
        request = ("CREATE TABLE IF NOT EXISTS {} ({} SERIAL PRIMARY KEY, {} text UNIQUE);").format(self._fingerprint_table, self._id, self._fingerprint)
        connection.execute(request)
        connection.commit()
    

    def get_id_by_value(self, fingerprint):
        connection = self._connection_factory.create_connection()
        request = ("SELECT {} FROM {} WHERE {} = '{}';").format(self._id, self._fingerprint_table, self._fingerprint, fingerprint)
        connection.execute(request)
        result = connection.fetch()
        if not result:
            return None
        return result[0]

    def add_value(self, fingerprint):
        connection = self._connection_factory.create_connection()
        request = ("INSERT INTO {}({}) VALUES ({});").format(self._fingerprint_table, self._fingerprint, fingerprint)
        connection.execute(request)
        connection.commit()

    def _safe_info(self, json_data, column_list):
        connection = self._connection_factory.create_connection()
        values = []
        for column in column_list:
            values.append(json_data[column])
        
        request = ("INSERT INTO {}({}) VALUES ({});").format(self._fingerprint_table, ', '.join(column_list), ', '.join(values))
        connection.execute(request)
        connection.commit()
