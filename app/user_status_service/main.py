from statistics_manager import *
from data_publisher import *
import cherrypy
import logging
from bs4 import BeautifulSoup as bs


@cherrypy.expose
class Main:
    def __init__(self):
        self.manager = StatisticsManager()
        self.id_service_conf = ConnectionConfigurationManager.create_service_conf()
        self.publisher = DataPublisher()

    @cherrypy.expose
    def index(self):
        index = open("/app/data/index.html").read()
        logging.info("index")
        return index

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def update(self):
        data = cherrypy.request.json
        headers = self.get_headers()
        params = {**data, **headers}
        logging.info("got data" + data)
        fp_id = self.get_id(params)
        status = self.manager.get_user_status(fp_id).name
        name = self.manager.get_user_name(fp_id)
        self.manager.update(fp_id, name)
        if name is None:
            page = open("/app/data/new_user.html").read()
            soup = bs(page, 'html.parser')
            title = soup.find("fingerprint")
            title.text = fp_id
            return soup.prettify("utf-8")
        page = open("/app/data/welcome.html").read()
        soup = bs(page, 'html.parser')
        title = soup.find("title")
        title.text.format(name)
        return soup.prettify("utf-8")

    @cherrypy.expose
    def register(self):
        name = cherrypy.request.params.get('name')
        fp = cherrypy.request.params.get('fingerprint')
        self.manager.update(fp, name)

    @staticmethod
    def get_headers():
        data = cherrypy.request.headers
        return data

    def get_id(self, params):
        connection = self.id_service_conf.create_connection()
        return connection.get_id(params)
