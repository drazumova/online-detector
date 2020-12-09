from fingerprint_database import *

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
        # print(json_data.keys())
        args = set(json_data.keys()).intersection(self.args)
        for arg in args:
            string_value += json_data[arg]
        return self.get_hash(string_value)