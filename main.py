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

    def PUT(self, id):
        self.manager.update_time(id)
        return "OK"

if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(Main(), '/', conf)