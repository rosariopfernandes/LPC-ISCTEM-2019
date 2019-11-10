class VariableDeclaration(object):
    data_type: str
    variable_name: str
    value: any

    def __init__(self, data_type, name, value=None):
        self.data_type = data_type
        self.variable_name = name
        self.value = value
