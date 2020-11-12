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
            id = self.get_id(self.get_headers())
        return self.manager.get_user_status(id).name

    def POST(self, id=None):
        if id is None:
            id = self.get_id(self.get_headers())
        self.manager.update_time(id)
        return "OK"

    def get_headers(self):
        data = cherrypy.request.headers
        return data

    def get_id(self, headers):
        return self.id_service_connection.get_id(headers)
