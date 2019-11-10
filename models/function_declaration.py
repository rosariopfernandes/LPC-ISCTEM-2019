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
