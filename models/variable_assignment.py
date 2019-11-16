class VariableAssignment(object):
    variable_name: str
    value: any

    def __init__(self, variable_name: str, value: str):
        self.variable_name = variable_name
        self.value = value

    def to_dict(self):
        return {
            'variable_name': self.variable_name,
            'value': self.value
        }
