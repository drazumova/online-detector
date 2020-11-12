import requests
import json

class FingerprintServiceConnection:
    headers_key = "passed_headers"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.Session()

    def get_id(self, headers):
        print("headers = ", headers)
        url = "http://{}:{}".format(self.host, self.port)
        data = {self.headers_key : headers}
        response = self.session.post(url, data=json.dumps(data))
        print("aaa", response.text)
        return json.loads(response.text)['id']



