import sys
sys.path.append('connection/')

from connection import *
class Database:
    _fingerprint_table = 'fingerprints'
    _id = 'id'
    _fingerprint = 'fingerprint'
    _params = [] # saved parameters for fingerprint counting

    def __init__(self, connection):
        self._connection = connection
        self.init_table()

    def init_table(self):
        request = ("CREATE TABLE IF NOT EXISTS {} ({} int PRIMARY KEY, {} text UNIQUE);").format(self._fingerprint_table, self._id, self._fingerprint)
        self._connection.execute(request)
        self._connection.commit()
    
    def get_id_by_value(self, fingerprint):
        request = ("SELECT {} FROM {} WHERE {} = {};").format(self._id, self._fingerprint_table, self._fingerprint, fingerprint)
        self._connection.execute(request)
        result = self._connection.fetch()
        if not result:
            return None
        return result[0]

    def add_value(self, fingerprint):
        request = ("INSERT INTO {}({}) VALUES ({});").format(self._fingerprint_table, self._fingerprint, fingerprint)
        self._connection.execute(request)
        self._connection.commit()

    def _safe_info(self, json_data, column_list):
        values = []
        for column in column_list:
            values.append(json_data[column])
        
        request = ("INSERT INTO {}({}) VALUES ({});").format(self._fingerprint_table, ', '.join(column_list), ', '.join(values))
        self._connection.execute(request)
        self._connection.commit()

