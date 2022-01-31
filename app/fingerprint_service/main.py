from fingerprint_manager import *
import cherrypy
from connection.fingerprint_service_connection import FingerprintServiceConnection
import json


@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = FingerprintManager()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        print("FP MAIN POST DATA:", cherrypy.request.json, flush=True)
        headers = cherrypy.request.json
        # if headers is None or FingerprintServiceConnection.headers_key not in headers.keys():
        #     return None
        # return json.dumps({'id': self.manager.get_id_with_closest(headers[FingerprintServiceConnection.headers_key])})
        return json.dumps({'id': self.manager.get_id_with_closest(headers)})
