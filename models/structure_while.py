class StructureWhile(object):
    condition: str
    assignments: list

    def __init__(self):
        self.condition = ''
        self.assignments = []

    def to_dict(self):
        _dict_assignments = []
        for assignment in self.assignments:
            _dict_assignments.append(assignment.to_dict())
        return {
            'condition': self.condition,
            'assignments': _dict_assignments
        }
