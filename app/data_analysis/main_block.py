import csv
import requests
import json

header_args = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr']
js_args = ['fonts', 'domBlockers', 'fontPreferences', 'audio', 'screenFrame', 'osCpu', 'languages', 'colorDepth',
               'deviceMemory', 'screenResolution', 'hardwareConcurrency', 'timezone', 'sessionStorage', 'localStorage',
               'indexedDB', 'openDatabase', 'cpuClass', 'platform', 'plugins', 'touchSupport', 'vendor',
               'vendorFlavors', 'cookiesEnabled', 'colorGamut', 'invertedColors', 'forcedColors', 'monochrome',
               'contrast', 'reducedMotion', 'hdr', 'math']
headers = ['_id', 'host', 'dnt', 'user-agent', 'accept', 'accept-encoding',
           'accept-language', 'ad', 'canvas', 'cookies', 'font-flash', 'language-flash',
           'platform-flash', 'languages-js', 'platform', 'plugins', 'screen_width', 'screen_height',
           'screen_depth', 'storage_local', 'storage_session', 'timezone',
           'userAgent-js', 'webGLVendor', 'webGLRenderer', 'timestamp']


def mapFP(row):
    names_map = {
        'User-Agent': 'user-agent',
        'Dnt': 'dnt',
        'Accept': 'accept',
        'Accept-Encoding': 'accept-encoding',
        'Accept-Language': 'accept-language',
        'domBlockers': 'ad',
        'platform': 'platform-flash',
        'cookiesEnabled': 'cookies',
        'sessionStorage': 'storage_session',
        'localStorage': 'storage_local',
        'Remote-Addr': 'host',
        'timezone': 'timezone',
        'webGL_vendor': 'webGLVendor',
        'webGL_renderer': 'webGLRenderer'
    }
    result = {}
    for key in names_map.keys():
        result[key] = {'value': row[names_map[key]]}
    result['canvas'] = {'value': {'geometry': row['canvas']}}
    return {'components': result}


def post_data(i, generated_ids):
    ids.add(i['_id'])
    data = mapFP(i)
    print("DATA", data)
    post_response = requests.post('http://192.168.39.68:30037', data=data, headers={'Content-Type': "application/json"})
    print("RESPONSE", post_response, flush=True)
    id = json.loads(post_response.text)['id']
    generated_ids.append((id, i['_id']))


if __name__ == '__main__':
    with open('fp-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        ids = set()
        generated_ids = []
        for i in [next(reader)]:
            post_data(i, generated_ids)
        print("generated_ids", "\n".join(generated_ids), sep="\n")
