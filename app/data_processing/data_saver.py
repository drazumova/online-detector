import json
import sys
sys.path.append('connection/')

from clickhouse_database import *
from clickhouse_connection import *
from rabbit_connection import *


class DataSaver:
    def __init__(self):
        self.clickhouse_conf = ClickHouseConnectionConfigurationManager.create_database_conf()
        self.database = ClickHouseDatabase(self.clickhouse_conf)

    def store(self, data):
        id = data.keys()[0]
        print("keeys = ", data.keys())
        data = data[id]
        args = set(data.keys()).intersection(ClickHouseDatabase.fileds_list)
        fields = [data[arg] for arg in args]
        self.database.store(id, data)
        

def get(ch, method, properties, body):  
    data_saver = DataSaver() #todo
    print("body = ", body)
    data = json.loads(body)
    data_saver.store(data)

if __name__== '__main__':
    print("Started")
    conf = RabbitConnectionConfigurationManager.create_rabbit_conf()
    connection = conf.create_connection(RabbitConnectionConfig.storing_queue)
    connection.start_consuming(RabbitConnectionConfig.storing_queue, get)

