class FunctionDeclaration(object):
    _data_type: str
    _function_name: str
    _value: any

    def __init__(self, data_type, name, value=None):
        self._data_type = data_type
        self._function_name = name
        self._value = value

    def get_data_type(self):
        return self._data_type

    def get_name(self):
        return self._function_name

    def get_value(self):
        return self._value
