class FunctionDeclaration(object):
    data_type: str
    function_name: str
    assignments: list
    local_declarations: list
    arguments: list
    return_value: str

    def __init__(self, data_type, name):
        self.data_type = data_type
        self.function_name = name
        self.assignments = []
        self.local_declarations = []
        self.arguments = []
        self.return_value = None

    def to_dict(self):
        _dict = {
            'data_type': self.data_type,
            'function_name': self.function_name,
            'return_value': self.return_value
        }
        _dict_assignments = []
        _dict_declarations = []
        _dict_arguments = []
        for assignment in self.assignments:
            _dict_assignments.append(assignment.to_dict())
        for declaration in self.local_declarations:
            _dict_declarations.append(declaration.to_dict())
        for argument in self.arguments:
            _dict_arguments.append(argument.to_dict())
        _dict['assignments'] = _dict_assignments
        _dict['local_declarations'] = _dict_declarations
        _dict['arguments'] = _dict_arguments
        return _dict
