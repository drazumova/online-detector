from connection.fp_connection import FingerprintConnectionConfigurationManager
from fingerprint_counter import *
from fingerprint_database import *
from fingerprint_values_database import *


class FingerprintManager:
    def __init__(self):
        self._counter = FingerprintCounter()
        conf = FingerprintConnectionConfigurationManager.create_database_conf()
        self._database = Database(conf)
        params = self._counter.parameter_parsers
        self._value_database = ValuesDatabase(params, conf)

    def get_id(self, data):
        fp = self._counter.calculate(data)
        id = self._database.get_id_by_value(fp)
        if id is None or len(id) != 1:
            self._database.add_value(fp)
            return self.get_id(data) #todo
        return id[0]

    def get_id_with_closest(self, data):
        # fp = self._counter.calculate(data)
        possible_fp = self._value_database.find_closest(data, 3)
        if possible_fp is None:
            return self.get_id(data)
        id = self._database.get_id_by_value(possible_fp)
        print("got id", id)
        if id is None:
            print("ERROR empty existing data")
        return id[0]
