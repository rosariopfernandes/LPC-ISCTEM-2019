class StructureIf(object):
    condition: str
    assignments: list

    def __init__(self):
        self.condition = ''
        self.assignments = []

    def to_dict(self):
        return {
            'condition': self.condition,
            'assignments': self.assignments
        }
