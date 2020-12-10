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
        data = data[id]
        args = set(data.keys()).intersection(ClickHouseDatabase.fileds_list)
        fields = [data[arg] for arg in args]
        self.database.store(id, data)
        

def get(ch, method, properties, body):
    data_saver = DataSaver() #todo
    print(body)
    data_saver.store(body)

if __name__== '__main__':
    connection = RabbitConnectionConfigurationManager.create_rabbit_conf()
    connection.start_consuming(RabbitConnectionConfig.storing_queue, get)

