from fingerprint_paramter import Parameter


class ValuesDatabase:
    _fingerprint_table = 'fingerprint_values'
    _id = "id"
    _fp = 'fingerprint'
    _stable_fp = 'stable_fp'

    def __init__(self, parameter_parsers, connection_factory):
        self._connection_factory = connection_factory
        self.parsers = parameter_parsers
        self.params = list(map(lambda x: x.name.replace('-', ''), parameter_parsers))
        self.init_params_table()

    def init_params_table(self):
        connection = self._connection_factory.create_connection()
        columns = ', '.join(["{} text".format(i) for i in self.params])
        connection.execute("drop table if exists {}".format(self._fingerprint_table))
        request = ("CREATE TABLE IF NOT EXISTS {} ({} SERIAL PRIMARY KEY, {} text, {} text, {});").format(
            self._fingerprint_table, self._id, self._fp, self._stable_fp, columns)
        print("creating table", request)
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
        column_values = self._values_to_str(fp, values)
        print("Add values", column_values)
        request = "INSERT INTO {}( VALUES ('{}');".format(self._fingerprint_table,
                                                          self._fingerprint_table, column_values)
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
        print("constructed function = ", function)
        all_columns = ", ".join(self.params)
        query = "SELECT {} FROM {} ORDER BY distance({}) LIMIT {}".format(self._id, self._fingerprint_table,
                                                                          all_columns, limit)
        request = function + query
        connection = self._connection_factory.create_connection()
        connection.execute(request)
        result = connection.fetch()
        connection.close()
        print("result", result)
        if result is None or len(result) < 1:
            return None
        return result[0]

    def find_all_by_stable(self, stable_fp):
        print("got stable fp", stable_fp, flush=True)
        where_statement = ' {} = {} '.format(self._stable_id, stable_fp)
        select_statement = '{}, {}, {}'.format(self._id, self._stable_id, ", ".join(self._variable_params))
        query = 'SELECT {} FROM {} WHERE {}'.format(select_statement, self._fingerprint_table, where_statement)
        print("got query ", query)

        connection = self._connection_factory.create_connection()
        connection.execute(query)
        result = connection.fetch()
        connection.close()

        for r in result:
            print(r)

        return result



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
        print("creating table", request)
        connection.execute(request)
        connection.commit()
        connection.close()