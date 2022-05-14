import csv
import logging

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
        'webGL_renderer': 'webGLRenderer',
    }
    result = {}
    for key in names_map.keys():
        result[key] = {'value': row[names_map[key]]}
    result['canvas'] = {'value': {'geometry': row['canvas']}}
    result['screenResolution'] = {'value': row['screen_width'] + 'x' + row['screen_width']}
    logging.info("screenResolution:", result['screenResolution'])
    return result


def post_data(i, generated_ids, fout):
    ids.add(i['_id'])
    data = mapFP(i)
    post_response = requests.post('http://192.168.39.68:30037', data=json.dumps(data), headers={'Content-Type': "application/json"})
    print(post_response.text, flush=True)
    response = json.loads(json.loads(post_response.text))
    id = response['id']
    generated_ids.append((id, i['_id']))
    print(id, i['_id'], file=fout)


if __name__ == '__main__':
    with open('fp-data.csv') as csvfile:
        fout = open("out_6.txt", "w")
        reader = csv.DictReader(csvfile)
        ids = set()
        generated_ids = []
        # print(reader.fieldnames)
        cnt = 0
        for i in reader:
            # if cnt > 1:
            #     break
            post_data(i, generated_ids, fout)
            cnt += 1

        fp_cnt = len(set([a for (a, b) in generated_ids]))
        true_fp_cnt = len(set([b for (a, b) in generated_ids]))
        len = len(generated_ids)
        print(fp_cnt, true_fp_cnt, len, file=fout)
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        fout.close()
        # for (a_i, b_i) in generated_ids:
        #     for (a_j, b_j) in generated_ids:
        #         if b_i == b_j and a_i == a_j:
        #             tp += 1
        #         elif b_i == b_j and a_i != a_j:
        #             fn += 1
        #         elif b_i != b_j and a_i != a_j:
        #             tn += 1
        #         else:
        #             fp += 1
        # print("generated_ids", "\n".join(["{}, {}\n".format(a, b) for (a, b) in generated_ids]), sep="\n")
        # print((tp + tn)/(tn + tp + fp + fn))
