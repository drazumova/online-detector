import logging

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
        stable = self._counter.stable_param_parsers
        stable_names = [i.name for i in stable]
        unstable = [i for i in params if i.name not in stable_names]
        self._value_database = ValuesDatabase(params, unstable, conf)

    def get_id(self, data):
        fp = self._counter.calculate(data)
        id = self._database.get_id_by_value(fp)
        if id is None or len(id) != 1:
            self._database.add_value(fp)
            return self.get_id(data) #todo
        return id[0]

    def get_id_with_closest(self, data):
        fp = self._counter.calculate_stable(data)
        possible_fp = self._value_database.find_all_by_stable(fp, data)
        logging.info("FP possible rows: ", possible_fp)
        if possible_fp is None:
            logging.error("ERROR empty existing data")
            self._value_database.add(fp, data)
            fp = self._value_database.find_all_by_stable(fp, data)  # todo
            logging.info('fp after add',  fp)
            return fp

        return possible_fp
