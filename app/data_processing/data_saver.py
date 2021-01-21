import json
import sys
sys.path.append('connection/')

from clickhouse_database import *
from clickhouse_connection import *
from rabbit_connection import *

from logger import Logger


class DataSaver:
    def __init__(self):
        self.clickhouse_conf = ClickHouseConnectionConfigurationManager.create_database_conf()
        self.database = ClickHouseDatabase(self.clickhouse_conf)

    def store(self, data):
        id = data['Fp_Id']
        self.database.store(id, data)
        

def get(ch, method, properties, body):  
    data_saver = DataSaver() #todo
    data = json.loads(body)
    Logger.log("body = " + str(data))
    data_saver.store(data)

if __name__== '__main__':
    Logger.log("DataSaver start")
    conf = RabbitConnectionConfigurationManager.create_rabbit_conf()
    connection = conf.create_connection(RabbitConnectionConfig.storing_queue)
    connection.start_consuming(RabbitConnectionConfig.storing_queue, get)

