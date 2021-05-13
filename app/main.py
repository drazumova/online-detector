from logic import *
import cherrypy

@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = StatisticsManager()

    def GET(self, id=None):
        if id is None:
            return Status.UNKNOWN.name
        return self.manager.get_user_status(id).name

    def POST(self, id):
        self.manager.update_time(id)
        return "OK"
