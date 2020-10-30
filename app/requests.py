from logs import *
import json
import ssl
import requests

if __name__=='__main__':
    file = open('logs.txt', 'r')
    for request in file.readlines():
        params = json.loads(request)
        url = params['request']
        method = params['method']
        resp = "empty"
        if method == 'POST':
            resp = requests.post(url, headers = params['headers'], data = params['post_args'])
        elif method == 'GET':
            resp = requests.get(url, headers = params['headers'], data = params['get_args'])
        print(resp)
    file.close()

    