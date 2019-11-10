class ProcedureDeclaration(object):
    procedure_name: str
    assignments: list
    local_declarations: list

    def __init__(self, procedure_name: str, assignments: list):
        self.procedure_name = procedure_name
        self.assignments = assignments
        self.local_declarations = []
