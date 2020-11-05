from fingerprint import *
import cherrypy

@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = FingerprintManager()

    def POST(self):
        headers = cherrypy.request.data
        if headers is None:
            return None
        return self.manager.get_id(headers)
