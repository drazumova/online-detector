import sys
sys.path.append('connection/')

from connection_configuration import *
from fingerprint_counter import *

class FingerprintManager:
    def __init__(self):
        self._counter = FingerprintCounter()
        conf = FingerpritConnectionConfigurationManager.create_database_conf()
        self._database = Database(conf)

    def get_id(self, data):
        fp = self._counter.count(data)
        id = self._database.get_id_by_value(fp)
        if id is None or len(id) != 1:
            self._database.add_value(fp)
            return self.get_id(data) #todo
        return id[0]
