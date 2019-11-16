class ProcedureDeclaration(object):
    procedure_name: str
    assignments: list
    local_declarations: list
    arguments: list

    def __init__(self, procedure_name: str, assignments: list):
        self.procedure_name = procedure_name
        self.assignments = assignments
        self.local_declarations = []
        self.arguments = []

    def to_dict(self):
        _dict = {'procedure_name': self.procedure_name}
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
