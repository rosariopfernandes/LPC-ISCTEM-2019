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
