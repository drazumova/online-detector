import sys
sys.path.append('connection/')

from logic import *
from connection import *
import cherrypy

@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = StatisticsManager()
        self.id_service_connection = ConnectionManager().create_service_connection()

    def GET(self, id=None):
        if id is None:
            id = self.get_id(self.get_header())
        return self.manager.get_user_status(id)

    def POST(self, id=None):
        if id is None:
            id = self.get_id(self.get_header())
        self.manager.update_time(id)
        return "OK"

    def get_header(self):
        data = cherrypy.request.headers
        print("!!!", data)
        # data['Remote-Addr'] = cherrypy.request.remote
        # print(data)
        return data

    def get_id(self, headers):
        return self.id_service_connection.get_id(headers)
