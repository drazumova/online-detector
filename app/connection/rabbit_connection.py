import atexit
import pika
import yaml

from connection.connection_configuration import *


class RabbitConnection:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        atexit.register(self.close)

    def close(self):
        self.connection.close()

    def declare_queue(self, name):
        self.channel.queue_declare(queue=name)

    def basic_publish(self, key, data):
        self.channel.basic_publish(exchange="", routing_key=key, body=data)
    
    def start_consuming(self, key, callback):
        print("Start")
        self.channel.basic_consume(queue=key, auto_ack=True, on_message_callback=callback)
        self.channel.start_consuming()


class RabbitConnectionConfig(ConnectionConfig):
    storing_queue = "clickhouse"
    geoip_queue = "geoip"

    def __init__(self, filename):
        with open(filename, 'r') as config:
            args = yaml.load(config)
            self.host = args['host']

    def create_connection(self, queue):
        connection = RabbitConnection(self.host)
        connection.declare_queue(queue)
        return connection
    

class RabbitConnectionConfigurationManager(ConnectionConfigurationManager):
    @staticmethod
    def create_rabbit_conf(filename="app/connection/conf/rabbit_config.yaml"):
        return RabbitConnectionConfig(filename)
