class StructureIf(object):
    condition: str
    assignments: list
    else_assignments: list

    def __init__(self):
        self.condition = ''
        self.assignments = []
        self.else_assignments = []

    def to_dict(self):
        _dict_assignments = []
        _dict_else_assignments = []
        for assignment in self.assignments:
            _dict_assignments.append(assignment.to_dict())
        for assignment in self.else_assignments:
            _dict_else_assignments.append(assignment.to_dict())
        return {
            'condition': self.condition,
            'assignments': _dict_assignments,
            'else_assignments': _dict_else_assignments
        }

