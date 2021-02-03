import sys
sys.path.append('connection/')

from statistics_manager import *
from connection_configuration import *
from data_publisher import *
import cherrypy

@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = StatisticsManager()
        self.id_service_conf = ConnectionConfigurationManager.create_service_conf()
        self.publisher = DataPublisher()

    def GET(self, id=None, *args, **post):
        if id is None:
            id = self.get_id(self.get_headers())
        return self.manager.get_user_status(id).name

    def POST(self, id=None, *args, **post):
        headers = self.get_headers()
        if id is None:
            id = self.get_id(headers)
        self.manager.update_time(id)
        self.publisher.publish(id, headers)
        
        return "OK"

    def get_headers(self):
        data = cherrypy.request.headers
        print(str(data), flush=True)
        return data

    def get_id(self, headers):
        connection = self.id_service_conf.create_connection()
        return connection.get_id(headers)
