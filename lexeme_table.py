class Lexema(object):
    token: str
    classification: str
    line: int

    def __init__(self, token, classification, line):
        self.token = token
        self.classification = classification
        self.line = line


class LexemeTable(object):
    CLASSIFICATION_IDENTIFIER = 'Identificador'
    CLASSIFICATION_CONSTANT_NUMERIC = 'Constante numérica'
    CLASSIFICATION_CONSTANT_BOOLEAN = 'Valor booleano'
    CLASSIFICATION_CONSTANT_CHARACTER = 'Constante caracter'
    CLASSIFICATION_PRIMITIVE_TYPE = 'Tipo Primitivo'
    CLASSIFICATION_RESERVED_WORD = 'Palavra Reservada'
    CLASSIFICATION_SPECIAL_SYMBOL = 'Símbolo especial'
    CLASSIFICATION_UNKNOWN = 'Não reconhecido'

    _lexemes: list = []

    def add_boolean_constant(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_CONSTANT_BOOLEAN, line_number))

    def add_char_constant(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_CONSTANT_CHARACTER, line_number))

    def add_identifier(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_IDENTIFIER, line_number))

    def add_numeric_constant(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_CONSTANT_NUMERIC, line_number))

    def add_primitive_type(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_PRIMITIVE_TYPE, line_number))

    def add_reserved_word(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_RESERVED_WORD, line_number))

    def add_special_symbol(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_SPECIAL_SYMBOL, line_number))

    def add_unknown(self, word: str, line_number: int):
        self._lexemes.append(Lexema(word, self.CLASSIFICATION_UNKNOWN, line_number))

    def get_last_token(self):
        return self._lexemes[-1].token

    def get_second_last_token(self):
        return self._lexemes[-2].token

    def get_lexemes(self):
        return self._lexemes
