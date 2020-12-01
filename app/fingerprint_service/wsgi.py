import cherrypy
from main import Main

if __name__=='__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8091})
    cherrypy.quickstart(Main(), '/', conf)
