from statistics_manager import *
from data_publisher import *
import cherrypy
# import simplejson


@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = StatisticsManager()
        self.id_service_conf = ConnectionConfigurationManager.create_service_conf()
        self.publisher = DataPublisher()

    # def GET(self, id=None, *args, **post):
    #     if id is None:
    #         id = self.get_id(self.get_headers())
    #     return self.manager.get_user_status(id).name
    #
    # def POST(self, id=None, *args, **post):
    #     headers = self.get_headers()
    #     if id is None:
    #         id = self.get_id(headers)
    #     self.manager.update_time(id)
    #     self.publisher.publish(id, headers)
    #
    #     return "OK"

    @cherrypy.expose
    def index(self):
        index = open("/app/data/index.html").read()
        print("In index")
        return index

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def update(self):
        data = cherrypy.request.json
        headers = self.get_headers()
        params = {**data, **headers}
        fp_id = self.get_id(params)
        status = self.manager.get_user_status(fp_id).name
        self.manager.update_time(fp_id)
        return status

    @staticmethod
    def get_headers():
        data = cherrypy.request.headers
        return data

    def get_id(self, params):
        connection = self.id_service_conf.create_connection()
        return connection.get_id(params)
