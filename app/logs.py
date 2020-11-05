import json
from db import *

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


if __name__=='__main__':
    store_logs('logs.txt')
