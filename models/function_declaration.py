class FunctionDeclaration(object):
    data_type: str
    function_name: str
    assignments: list
    local_declarations: list

    def __init__(self, data_type, name, assignments: list):
        self.data_type = data_type
        self.function_name = name
        self.assignments = assignments
        self.local_declarations = []
