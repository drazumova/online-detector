import requests
import json


class FingerprintServiceConnection:
    headers_key = "passed_headers"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.Session()

    def get_id(self, headers):
        url = "http://{}:{}".format(self.host, self.port)
        response = self.session.post(url, data=json.dumps(headers),  headers={'Content-Type': "application/json"})
        try:
            return json.loads(json.loads(response.text))['id']
        except ValueError as e:
            print(e)
            return {}
