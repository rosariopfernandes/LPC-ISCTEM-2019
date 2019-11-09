class Identificador(object):
    identifier: str
    category: str
    data_type: str
    memory_structure: str
    value: str
    params_nr: int
    params_sequence: str
    evaluation_strategy: str
    reference: str
    level: str

    def __init__(self, identifier='-', category='-', data_type='-', memory_structure='-', value='-', params_nr='-',
                 params_sequence='-', evaluation_strategy='-', reference='-', level='-'):
        self.identifier = identifier
        self.category = category
        self.data_type = data_type
        self.memory_structure = memory_structure
        self.value = value
        self.params_nr = params_nr
        self.params_sequence = params_sequence
        self.evaluation_strategy = evaluation_strategy
        self.reference = reference
        self.level = level
