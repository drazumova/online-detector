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
        # print(self.name, data.keys())
        if self.name not in data.keys() or 'value' not in data[self.name].keys():
            return None
        return Parameter(self.get_value(data), self.name)

    def get_value(self, data):
        # print("getting", self.name, data['components'][self.name], flush=True)
        return data[self.name]['value']


class CanvasParameterParser(JSParameterParser):
    def get_value(self, data):
        return data[self.name]['value']['geometry']
