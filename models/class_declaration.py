class ClassDeclaration(object):
    class_name: str
    variable_declarations: list
    function_declarations: list
    procedure_declarations: list

    def __init__(self):
        self.class_name = 'undefined'
        self.variable_declarations = []
        self.function_declarations = []
        self.procedure_declarations = []

    def to_dict(self):
        _dict = {'class_name': self.class_name}
        _dict_variables = []
        _dict_functions = []
        _dict_procedures = []
        for variable in self.variable_declarations:
            _dict_variables.append(variable.to_dict())
        for _function in self.function_declarations:
            _dict_functions.append(_function.to_dict())
        for procedure in self.procedure_declarations:
            _dict_procedures.append(procedure.to_dict())
        _dict['variable_declarations'] = _dict_variables
        _dict['function_declarations'] = _dict_functions
        _dict['procedure_declarations'] = _dict_procedures
        return _dict
