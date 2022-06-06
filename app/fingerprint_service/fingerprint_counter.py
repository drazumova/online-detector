from fingerprint_paramter import *
import numpy as np


class FingerprintCounter:
    header_args = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr']
    js_args = ['fonts', 'domBlockers', 'fontPreferences', 'audio', 'screenFrame', 'osCpu', 'languages', 'colorDepth',
               'deviceMemory', 'screenResolution', 'hardwareConcurrency', 'timezone', 'sessionStorage', 'localStorage',
               'indexedDB', 'openDatabase', 'cpuClass', 'platform', 'touchSupport', 'vendor',
               'vendorFlavors', 'cookiesEnabled', 'colorGamut', 'invertedColors', 'forcedColors', 'monochrome',
               'contrast', 'reducedMotion', 'hdr', 'math', 'webGL_vendor', 'webGL_renderer']
    stable_params = ['osCpu', 'hardwareConcurrency', 'touchSupport', 'screenResolution', 'domBlockers',
                     'audio', 'languages', 'colorDepth', 'indexedDB', 'openDatabase', 'cpuClass', 'vendor',
                     'vendorFlavors', 'cookiesEnabled', 'invertedColors', 'forcedColors', 'canvas',
                     'reducedMotion', 'hdr', 'fonts', 'timezone', 'webGL_vendor', 'webGL_renderer']
    variable_params = list(set(js_args) - set(stable_params))

    def __init__(self):
        self.parameter_parsers = list(map(JSParameterParser, self.header_args)) \
                                 + list(map(JSParameterParser, self.js_args)) \
                                 + [PluginsParameterParser('plugins')] \
                                 + [CanvasParameterParser('canvas')]
        self.stable_param_parsers = list(map(JSParameterParser, self.stable_params)) + [CanvasParameterParser('canvas')]

    @staticmethod
    def get_hash(string):
        return xxhash.xxh3_128_hexdigest(string)

    def parameter_names(self):
        return [i.name for i in self.parameter_parsers]

    def _get_params(self, data):
        return [parser.parse_from_json(data) for parser in self.parameter_parsers]

    def get_stable_params(self, data):
        return [parser.parse_from_json(data) for parser in self.stable_param_parsers]

    def string_representation(self, data):
        return {parser.name: parser.parse_from_json(data) for parser in self.parameter_parsers}

    def params_to_hash(self, params):
        param_string = ';'.join([Parameter.to_string(value) for value in params])
        # param_string = str([Parameter.to_string(value) for value in params])
        resulting_hash = self.get_hash(param_string)
        return resulting_hash

    # def distance(self, data, row, weights):
    #     return np.sum(weights * (row == data))

    def get_unstable_param_parsers(self):
        return [i for i in self.parameter_parsers if i not in self.stable_param_parsers]

    def calculate_stable(self, data):
        params = self.get_stable_params(data)
        return self.params_to_hash(params)

    def calculate(self, json_data):
        params = self._get_params(json_data)
        return self.params_to_hash(params)
