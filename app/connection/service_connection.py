import requests

class FingerprintServiceConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.Session()

    def get_id(self, headers):
        print("headers = ", headers)
        url = "http://{}:{}".format(self.host, self.port)
        response = self.session.post(url, data=headers)
        print("response = ", response.message)
        return int(response.text['id'])



