import logging

import xxhash


class Parameter:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def get_info(self):
        return self.name, self.value

    @staticmethod
    def to_string(value):
        if value is None or not isinstance(value, Parameter):
            return ""
        return value.get_hash()

    def get_hash(self):
        return xxhash.xxh3_128_hexdigest(str(self.value))


class ParameterParser:
    def __init__(self, name):
        self.name = name

    def get_value(self, data):
        return data[self.name]

    def parse_from_json(self, data):
        if self.name not in data.keys():
            return None
        return Parameter(self.get_value(data), self.name)


class JSParameterParser(ParameterParser):
    def parse_from_json(self, data):
        if self.name not in data['components'].keys() or 'value' not in data['components'][self.name].keys():
            return None
        return Parameter(self.get_value(data), self.name)

    def get_value(self, data):
        return data['components'][self.name]['value']


class CanvasParameterParser(JSParameterParser):
    def get_value(self, data):
        return data['components'][self.name]['value']['geometry']


class PluginsParameterParser(JSParameterParser):
    def get_value(self, data):
        all = data['components'][self.name]['value']
        names = []
        for plugin_def in all:
            names.append(plugin_def["name"])
        logging.info("got plugin names", names)
        return ",".join(names)
