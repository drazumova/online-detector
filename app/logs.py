import json
from db import *
import xxhash

def parse(filename, args=None):
    file = open(filename, "r")
    result = []
    for line in file.readlines():
        request = {}
        data = json.loads(line)['headers']
        
        if (args == None):
            result.append(data)
            continue
        print(data)
        for arg in args:
            request[arg] = data[arg]
        result.append(request)
    
    file.close()
    return result
    
def store_logs(filename):
    database = Database(DatabaseConnectionManager().create_connection())
    counter = FingerprintCounter()
    values = counter.process_logs(filename)
    column_names = counter.args + ["id"]
    for value in values:
        database.safe_info(value, column_names)


class FingerprintCounter:
    args = ['user-agent', 'accept-language']
    
    def process_logs(self, filename):
        all_requests = parse(filename, self.args)
        print(all_requests)
        for i in range(len(all_requests)):
            id = self.count(all_requests[i])
            all_requests[i]["id"] = id

        return all_requests

    def get_hash(self, str):
        return xxhash.xxh32(b'Nobody inspects the spammish repetition').intdigest()

    def count(self, json_data):
        string_value = ""
        print(json_data)
        for arg in self.args:
            string_value += json_data[arg]
        return self.get_hash(string_value)



if __name__=='__main__':
    store_logs('logs.txt')
