class Identifier(object):
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

    def __init__(self, identifier='-', category='-', data_type='-', memory_structure='-', value='-', params_nr=0,
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

    def to_dict(self):
        return {
            'identifier': self.identifier,
            'category': self.category,
            'data_type': self.data_type,
            'evaluation_strategy': self.evaluation_strategy,
            'level': self.level,
            'memory_structure': self.memory_structure,
            'params_nr': self.params_nr,
            'params_sequence': self.params_sequence,
            'reference': self.reference,
            'value': self.value,
        }


class IdentifierTable(object):
    CATEGORY_CLASS = 'Classe'
    CATEGORY_VARIABLE = 'Variavel'
    CATEGORY_METHOD = 'Metodo'
    CATEGORY_PARAMETER = 'Parametro'

    _identifiers: list

    def __init__(self):
        self._identifiers = []

    def add_class(self, identifier: str, level: float):
        self._identifiers.append(Identifier(identifier=identifier, category=self.CATEGORY_CLASS, level=str(level)))

    def add_variable(self, identifier: str, data_type: str, value: str, reference: str, level: float):
        self._identifiers.append(Identifier(identifier=identifier, category=self.CATEGORY_VARIABLE,
                                            data_type=data_type, memory_structure='Primitivo', value=value,
                                            evaluation_strategy='-', reference=reference,
                                            level=str(level)))

    def add_method(self, identifier: str, data_type: str, parameter_count: int, parameter_sequence: str,
                   reference: str, level: float):
        self._identifiers.append(Identifier(identifier=identifier, category=self.CATEGORY_METHOD,
                                            data_type=data_type, memory_structure='Primitivo',
                                            params_nr=parameter_count, params_sequence=parameter_sequence,
                                            reference=reference, level=str(level)))

    def add_parameter(self, identifier: str, data_type: str, value: str, reference: str, level: float):
        self._identifiers.append(Identifier(identifier=identifier, category=self.CATEGORY_PARAMETER,
                                            data_type=data_type, memory_structure='Primitivo',
                                            evaluation_strategy='Por valor',
                                            value=value, reference=reference, level=str(level)))

    def index_of(self, identifier: str):
        for i in range(0, len(self._identifiers)):
            if self._identifiers[i].identifier == identifier:
                return i
        return -1

    def contains(self, identifier: str):
        for identificador in self._identifiers:
            if identificador.identifier == identifier:
                return True
        return False

    def has_been_declared(self, identifier: str, level: float):
        for identificador in self._identifiers:
            if identificador.identifier == identifier and float(identificador.level) == level:
                return True
        return False

    def get_identifiers(self):
        return self._identifiers

    def update_params_nr(self, index: int, parameter_count: int):
        self._identifiers[index].params_nr = parameter_count

    def update_params_sequence(self, index: int, parameter_sequence: str):
        self._identifiers[index].params_sequence = parameter_sequence

    def update_value(self, index: int, new_value: str):
        self._identifiers[index].value = new_value

    def to_dict(self):
        _dic_list = []
        for symbol in self._identifiers:
            _dic_list.append(symbol.to_dict())
        return _dic_list
