from logger import Logger


class ClickHouseDatabase:
    _table = "storage"
    _fingerprint_id = "Fingerprint_ID"
    _fields_list = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr', 'X-Real-Ip']
     
    def __init__(self, connection_factory, additional_fields=[]):
        self._connection_factory = connection_factory  
        self._all_fields = self._fields_list + additional_fields
        self.init_table() 
    
    def init_table(self):
        connection = self._connection_factory.create_connection()
        # connection.execute("drop table {}".format(self._table))
        columns = "{} UInt64, {}".format(self._fingerprint_id, ", ".join(map(lambda x: x + " String", self._all_fields)))
        request = ("CREATE TABLE IF NOT EXISTS {} ({}) ENGINE = MergeTree() ORDER BY {}").format(self._table, columns.replace("-", "_"), self._fingerprint_id)
        Logger.log(request)
        connection.execute(request)
    
    def store(self, fingerprint_id, data):
        allowed_keys = self._all_fields
        keys = [key for key in data.keys() if key in allowed_keys]
        fields = [data[key] for key in keys]
        connection = self._connection_factory.create_connection()
        column_list = self._fingerprint_id + ", " + ", ".join(keys).replace("-", "_")
        value_list =  ", ".join(map(lambda x: "'" + x + "'", fields))
        request = "INSERT INTO {}({}) VALUES ({}, {})".format(self._table, column_list, fingerprint_id, value_list)
        Logger.log(request)
        connection.execute(request)
