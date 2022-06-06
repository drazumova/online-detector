import logging

import numpy as np

from fingerprint_paramter import Parameter


class ValuesDatabase:
    _fingerprint_table = 'fingerprint_values'
    _id = "id"
    _fp = 'fingerprint'
    _stable_fp = 'stable_fp'
    _weights = []

    def __init__(self, parameter_parsers, unstable_parameter_parsers,  connection_factory):
        self._connection_factory = connection_factory
        self.parsers = parameter_parsers
        self._unstable_columns = list(map(lambda x: x.name.replace('-', '').lower(), unstable_parameter_parsers))
        self._unstable_parsers = unstable_parameter_parsers
        self.params = list(map(lambda x: x.name.replace('-', '').lower(), parameter_parsers))
        self.init_params_table()

    def init_params_table(self):
        connection = self._connection_factory.create_connection()
        columns = ', '.join(["{} text".format(i) for i in self.params])
        connection.execute("drop table if exists {}".format(self._fingerprint_table))
        request = ("CREATE TABLE IF NOT EXISTS {} ({} SERIAL PRIMARY KEY, {} text, {} text, {});").format(
            self._fingerprint_table, self._id, self._fp, self._stable_fp, columns)
        logging.info("creating table", request)
        connection.execute(request)
        connection.commit()
        connection.close()

    @staticmethod
    def _values_to_str(fp, values):
        wrapped_values = ["'{}'".format(i) for i in values]
        column_values = "'{}', {}".format(fp, ', '.join(wrapped_values))
        return column_values

    def add(self, fp, values):
        connection = self._connection_factory.create_connection()
        column_values = ', '.join(["'{}'".format(Parameter.to_string(p.parse_from_json(values))) for p in self.parsers])
        logging.info("Add values", column_values)

        columns = ', '.join([i for i in self.params])
        column_names = "{}, {}".format(self._stable_fp, columns)
        logging.info(column_names, column_values)
        request = "INSERT INTO {} ({}) VALUES ('{}', {});".format(self._fingerprint_table,
                                                                    column_names,
                                                                    fp, column_values)
        connection.execute(request)
        connection.commit()
        connection.close()

    def find_closest(self, values, limit):
        function_params = ', '.join(map(lambda name: name + " text", self.params))
        function_value = ' + '.join(["({} <> '{}')".format(name, Parameter.to_string(parser.parse_from_json(values))) for (name, parser)
                                     in zip(self.params, self.parsers)])
        function = ("CREATE FUNCTION distance({}) RETURNS real " + \
                    "AS 'SELECT {};' LANGUAGE SQL IMMUTABLE RETURNS NULL ON NULL INPUT;") \
            .format(function_params, function_value)
        all_columns = ", ".join(self.params)
        select_statement = ""
        query = "SELECT {} FROM {} ORDER BY distance({}) LIMIT {}".format(select_statement, self._fingerprint_table,
                                                                          all_columns, limit)
        request = function + query
        connection = self._connection_factory.create_connection()
        connection.execute(request)
        result = connection.fetch()
        connection.close()
        if result is None or len(result) < 1:
            return None

        return result[0]

    def closest_for(self, data, result):
        weights = np.array([0] + self._weights)
        current = np.array([0] + [Parameter.to_string(i.parse_from_json(data)) for i in self._unstable_parsers])
        if current.shape[0] > weights.shape[0]:
            weights = np.append(weights, np.ones(current.shape[0] - weights.shape[0]))
        distances = np.dot((np.array(result) != current), weights)
        index = np.argmin(distances)
        if distances[index] > 2:
            return None
        return result[index][0]

    def find_all_by_stable(self, stable_fp, data, columns=""):
        if len(columns) == 0:
            columns = ", ".join(self._unstable_columns)
        logging.info("got stable fp ", stable_fp)
        where_statement = ' {} = \'{}\' '.format(self._stable_fp, stable_fp)
        select_statement = '{}, {}'.format(self._id, columns)
        query = 'SELECT {} FROM {} WHERE {}'.format(select_statement, self._fingerprint_table, where_statement)
        logging.info("got query ", query)

        connection = self._connection_factory.create_connection()
        connection.execute(query)
        result = connection.fetch()
        connection.close()

        for r in result:
            logging.info("got result row", r)

        if result is None or len(result) == 0:
            return None

        return self.closest_for(data, result)



class ValuesGroupsDatabase(ValuesDatabase):
    _fingerprint_table = 'fingerprint_values'
    _id = 'fingerprint'

    def __init__(self, parameter_names, change_probabilities, connection_factory):
        super.__init__(parameter_names, connection_factory)
        self.probabilities = change_probabilities
        pairs = zip(self.params, self.probabilities)
        self.params_map = {name: prob for (name, prob) in pairs}
        self.groups = [
            [name for (name, prob) in pairs if prob < 1], [name for (name, prob) in pairs if 20 > prob > 1],
            [name for (name, prob) in pairs if 20 < prob < 50], [name for (name, prob) in pairs if prob > 50]
        ]
        self.params = ["group_" + str(i) for i in range(len(self.groups))]

    def init_params_table(self):
        connection = self._connection_factory.create_connection()
        columns = ', '.join(["{} text".format(i) for i in self.params])
        request = ("CREATE TABLE IF NOT EXISTS {} ({} text PRIMARY KEY, {});").format(
            self._fingerprint_table, self._id, columns)
        logging.info("creating table", request)
        connection.execute(request)
        connection.commit()
        connection.close()