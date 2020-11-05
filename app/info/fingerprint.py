from fingerprint_db import *

import xxhash

class FingerprintCounter:
    args = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr']
    
    def process_logs(self, filename):
        all_requests = parse(filename, self.args)
        print(all_requests)
        for i in range(len(all_requests)):
            id = self.count(all_requests[i])
            all_requests[i]["id"] = id

        return all_requests

    def get_hash(self, str):
        return xxhash.xxh32(str).intdigest()

    def count(self, json_data):
        string_value = ""
        print(json_data.keys())
        args = intersection(json_data.keys(), self.args)
        for arg in args:
            string_value += json_data[arg]
        return self.get_hash(string_value)

class FingerprintManager:
    def __init__(self):
        connection = ConnectionManager().create_database_connection()
        self._database = Database(connection)
        self._counter = FingerprintCounter()

    def get_id(self, data):
        fp = self._counter(data)
        id = self._database.get_id_by_value(fp)
        if id is None:
            self._database.add_value(fp)
            return get_id(self, data) #todo
        return id