from fingerprint_manager import *
import cherrypy
from connection.fingerprint_service_connection import FingerprintServiceConnection
import json


@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = FingerprintManager()

    def POST(self):
        headers = json.loads(cherrypy.request.body.read())
        if headers is None or FingerprintServiceConnection.headers_key not in headers.keys():
            return None
        return json.dumps({'id': self.manager.get_id(headers[FingerprintServiceConnection.headers_key])})
