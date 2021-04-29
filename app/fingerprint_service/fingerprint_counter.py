from fingerprint_paramter import *


class FingerprintCounter:
    header_args = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr']
    js_args = ['audio', 'fonts', 'colorDepth', 'deviceMemory', 'screenResolution', 'hardwareConcurrency',
               'openDatabase', 'touchSupport', 'indexedDB']

    def __init__(self):
        self.parameter_parsers = list(map(ParameterParser, self.header_args)) \
                                 + list(map(JSParameterParser, self.js_args)) \
                                 + [CanvasParameterParser('canvas')]

    @staticmethod
    def get_hash(string):
        return xxhash.xxh64_hexdigest(string)

    def parameter_names(self):
        return [i.name for i in self.parameter_parsers]

    def _get_params(self, data):
        # print(data.keys())
        return [parser.parse_from_json(data) for parser in self.parameter_parsers]

    def calculate(self, json_data):
        params = self._get_params(json_data)
        param_string = str([Parameter.to_string(value) for value in params])
        resulting_hash = self.get_hash(param_string)
        print(resulting_hash, str(params))
        return resulting_hash
