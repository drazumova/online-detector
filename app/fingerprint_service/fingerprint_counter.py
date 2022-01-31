from fingerprint_paramter import *


class FingerprintCounter:
    header_args = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr']
    js_args = ['fonts', 'domBlockers', 'fontPreferences', 'audio', 'screenFrame', 'osCpu', 'languages', 'colorDepth',
               'deviceMemory', 'screenResolution', 'hardwareConcurrency', 'timezone', 'sessionStorage', 'localStorage',
               'indexedDB', 'openDatabase', 'cpuClass', 'platform', 'plugins', 'touchSupport', 'vendor',
               'vendorFlavors', 'cookiesEnabled', 'colorGamut', 'invertedColors', 'forcedColors', 'monochrome',
               'contrast', 'reducedMotion', 'hdr', 'math', 'webGL_vendor', 'webGL_renderer']
    stable_params = ['osCpu', 'hardwareConcurrency', 'touchSupport', 'screenResolution', 'domBlockers',
                     'audio', 'languages', 'colorDepth', 'indexedDB', 'openDatabase', 'cpuClass', 'vendor',
                     'vendorFlavors', 'cookiesEnabled', 'invertedColors', 'forcedColors', 'canvas',
                     'reducedMotion', 'hdr', 'fonts']
    variable_params = list(set(js_args) - set(stable_params))

    def __init__(self):
        self.parameter_parsers = list(map(ParameterParser, self.header_args)) \
                                 + list(map(JSParameterParser, self.js_args)) \
                                 + [CanvasParameterParser('canvas')]
        self.stable_param_parsers = list(map(JSParameterParser, self.stable_params))

    @staticmethod
    def get_hash(string):
        return xxhash.xxh64_hexdigest(string)

    def parameter_names(self):
        return [i.name for i in self.parameter_parsers]

    def _get_params(self, data):
        return [parser.parse_from_json(data) for parser in self.parameter_parsers]

    def get_stable_params(self, data):
        return [parser.parse_from_json(data) for parser in self.stable_param_parsers]

    def string_representation(self, data):
        return {parser.name: parser.parse_from_json(data) for parser in self.parameter_parsers}

    def calculate_stable(self, data):
        params = self.get_stable_params(data)
        param_string = str([Parameter.to_string(value) for value in params])
        resulting_hash = self.get_hash(param_string)
        print(resulting_hash, str(params))
        return resulting_hash

    def calculate(self, json_data):
        params = self._get_params(json_data)
        param_string = str([Parameter.to_string(value) for value in params])
        resulting_hash = self.get_hash(param_string)
        print(resulting_hash, str(params))
        return resulting_hash
