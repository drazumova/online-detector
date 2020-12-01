import sys
import json
sys.path.append('connection/')

from fingerprint_manager import *
import cherrypy
from fingerprint_service_connection import FingerprintServiceConnection as FC

@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = FingerprintManager()

    def POST(self):
        headers = json.loads(cherrypy.request.body.read())
        if headers is None or FC.headers_key not in headers.keys():
            return None
        return json.dumps({'id': self.manager.get_id(headers[FC.headers_key])})
