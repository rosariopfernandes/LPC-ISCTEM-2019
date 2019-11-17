from lexeme_table import LexemeTable
from identifier_table import IdentifierTable
from java_grammar import RESERVED_WORDS, PRIMITIVE_TYPES, SYMBOLS


class AuxiliarTables(object):
    # Tabelas
    _lexeme_table: LexemeTable
    _symbol_table: IdentifierTable

    # Variáveis auxiliares
    _current_line_number: int
    _is_comment: bool
    _is_parameter: bool
    _is_method_call_param: bool
    _last_data_type: str
    _level: float
    _parameter_count: int
    _parameter_sequence: str
    _variables_count: int
    _word: str

    def __init__(self):
        self._lexeme_table = LexemeTable()
        self._symbol_table = IdentifierTable()
        self._current_line_number = 1
        self._is_comment = False
        self._is_parameter = False
        self._is_method_call_param = False
        self._last_data_type = ''
        self._level = 0.0
        self._parameter_count = 0
        self._parameter_sequence = ''
        self._variables_count = 1
        self._word = ''

    # Funções auxiliares
    def _get_indentation(self, line: str):
        indentation = 0
        for char in line:
            if char == ' ':
                indentation += 1
            else:
                break
        return indentation

    def _is_real_number(self, word: str):
        # No caso de float
        if word[-1] == 'f':
            word = word[:-1]
        parts = word.split('.')
        if len(parts) > 2:
            return False
        for digit in parts:
            if not digit.isdigit():
                return False
        return True

    def _check_value(self):
        if self._lexeme_table.get_last_token() == '=':
            indice_identificador = self._symbol_table.index_of(self._lexeme_table.get_second_last_token())
            if indice_identificador != -1:
                self._symbol_table.update_value(indice_identificador, self._word)

    def _classify(self, word, line_number):
        # global parameter_count, parameter_sequence, variables_count, last_type
        if word != ' ' and word != '':
            if word in RESERVED_WORDS:
                self._lexeme_table.add_reserved_word(word, line_number)
            elif word in PRIMITIVE_TYPES:
                self._lexeme_table.add_primitive_type(word, line_number)
                self._last_data_type = word
            else:
                if self._lexeme_table.get_last_token() == 'class':
                    self._lexeme_table.add_identifier(word, line_number)
                    self._symbol_table.add_class(word, self._level)
                elif self._lexeme_table.get_last_token() in PRIMITIVE_TYPES:
                    if self._is_parameter:
                        self._lexeme_table.add_identifier(word, line_number)
                        self._parameter_count += 1
                        self._parameter_sequence += self._lexeme_table.get_second_last_token() + ', '
                        self._symbol_table.add_parameter(word, self._lexeme_table.get_second_last_token(), '-',
                                                         '', self._level)
                    else:
                        self._lexeme_table.add_identifier(word, line_number)
                        self._symbol_table.add_variable(word, self._lexeme_table.get_second_last_token(), '-', '',
                                                        self._level)
                elif self._lexeme_table.get_last_token() == ',':
                    # Várias variáveis na mesma linha
                    self._variables_count += 1
                    self._symbol_table.add_variable(word, self._last_data_type, '-', '', self._level)
                    self._lexeme_table.add_identifier(word, line_number)
                elif word.isdigit():
                    # constante do tipo inteiro
                    self._check_value()
                    self._lexeme_table.add_numeric_constant(word, line_number)
                elif word[-1:] == 'l':
                    # constante do tipo long
                    if word[:-1].isdigit():
                        self._check_value()
                        self._lexeme_table.add_numeric_constant(word[:-1], line_number)
                    else:
                        # self._lexeme_table.add_unknown(word, line_number)
                        return {
                            "code": -1,
                            "message": "Erro sintáctico: Token não esperado '" + self._word + "' na linha " +
                                       str(line_number)
                        }
                elif word == 'true' or word == 'false':
                    # constante do tipo booleano
                    self._check_value()
                    self._lexeme_table.add_boolean_constant(word, line_number)
                elif word.startswith('\'') and word.endswith('\'') and len(word) == 3:
                    # Verificar se esta constante está a ser atribuida à uma variável
                    self._check_value()
                    self._lexeme_table.add_char_constant(word, line_number)
                elif self._symbol_table.contains(word):
                    if not self._is_method_call_param:
                        self._lexeme_table.add_identifier(word, line_number)
                elif self._is_real_number(word):
                    self._lexeme_table.add_numeric_constant(word, line_number)
                else:
                    return {
                        "code": -1,
                        "message": "Erro sintáctico: Token não esperado '" + self._word + "' na linha " +
                                   str(line_number)
                    }
        return {
            "code": 200
        }

    # Funções públicas
    def execute(self, lines: list):

        for line in lines:
            self._level = self._get_indentation(line) / 40
            # TODO: round this value
            if self._level > 0.0:
                self._level -= 0.1
            self._word = ''
            for char in line:
                # Verificar se o comentário termina nesta linha
                if line.find('*/') != -1:
                    self._is_comment = False
                    break
                if self._is_comment:
                    # Ainda estamos em um comentário de várias linhas. Vamos saltar
                    self._word = ''
                    break
                if char == '*' and self._word == '/':
                    # Comentário de várias linhas. Vamos procurar onde termina
                    self._is_comment = True
                    self._word = ''
                    # Verificar se termina na mesma linha
                    if line.find('*/') != -1:
                        self._is_comment = False
                    break
                if char == '/' and self._word == '/':
                    # Comentário de uma linha. Vamos à próxima linha
                    self._word = ''
                    break
                if char in SYMBOLS:
                    self._lexeme_table.add_special_symbol(char, self._current_line_number)
                    self._word = ''
                elif char == ' ' or char == ';' or char == ',':
                    try:
                        response = self._classify(self._word, self._current_line_number)
                    except IndexError:
                        response = {
                            "code": -1,
                            "message": "Erro sintáctico: Token não esperado '" + self._word + "' na linha " +
                                       str(self._current_line_number)
                        }
                    if response.get("code") == -1:
                        return response
                    if char == ';':
                        self._variables_count = 0
                        self._last_data_type = ''
                    if char != ' ':
                        self._lexeme_table.add_special_symbol(char, self._current_line_number)
                    self._word = ''
                elif char == '(' and self._lexeme_table.get_last_token() in PRIMITIVE_TYPES:
                    # Início de um método.
                    self._symbol_table.add_method(self._word, self._lexeme_table.get_last_token(),
                                                  self._parameter_count, self._parameter_sequence, '', self._level)
                    self._lexeme_table.add_identifier(self._word, self._current_line_number)
                    self._lexeme_table.add_special_symbol(char, self._current_line_number)
                    # Vamos procurar parametros
                    self._word = ''
                    self._is_parameter = True
                elif char == '(' and (self._lexeme_table.get_last_token() == 'if' or
                                      self._lexeme_table.get_last_token() == 'while'):
                    # Abriu uma estrutura de controlo
                    self._lexeme_table.add_special_symbol(char, self._current_line_number)
                    self._word = ''
                elif char == ')':
                    if self._lexeme_table.get_last_token() in PRIMITIVE_TYPES:
                        # Temos um parametro
                        self._symbol_table.add_parameter(self._word, self._lexeme_table.get_last_token(), '', '',
                                                         self._level)
                        self._parameter_count += 1
                        self._parameter_sequence += self._lexeme_table.get_last_token()
                        self._lexeme_table.add_identifier(self._word, self._current_line_number)
                        self._word = ''
                    self._lexeme_table.add_special_symbol(char, self._current_line_number)
                    if self._parameter_sequence == '':
                        self._parameter_sequence = '-'
                    self._symbol_table.update_params_sequence(-(self._parameter_count + 1), self._parameter_sequence)
                    self._symbol_table.update_params_nr(-(self._parameter_count + 1), self._parameter_count)
                    self._parameter_sequence = ''
                    self._parameter_count = 0
                    self._is_parameter = False
                    self._is_method_call_param = False
                    self._word = ''
                elif char.isdigit():
                    char = str(char)
                    self._word += char
                else:
                    if char == '(':
                        if self._symbol_table.contains(self._word):
                            # Provavelmente está chamar um método
                            self._lexeme_table.add_identifier(self._word, self._current_line_number)
                            self._lexeme_table.add_special_symbol('(', self._current_line_number)
                            self._word = ''
                            self._is_method_call_param = True
                    else:
                        self._word += char
                    # Parametros passados ao método que está ser chamado
                    if self._symbol_table.contains(self._word) and self._is_method_call_param:
                        self._lexeme_table.add_identifier(self._word, self._current_line_number)
            self._current_line_number += 1
        return {
            "code": 200,
            "lexemes": self._get_lexemes_json(),
            "symbols": self._get_symbols_json()
        }

    def _get_lexemes_json(self):
        _dic_list = []
        for lexeme in self._lexeme_table.get_lexemes():
            _dic_list.append(lexeme.to_dict())
        return _dic_list

    def _get_symbols_json(self):
        _dic_list = []
        for symbol in self._symbol_table.get_identifiers():
            _dic_list.append(symbol.to_dict())
        return _dic_list

    def get_lexeme_table(self):
        return self._lexeme_table

    def get_symbol_table(self):
        return self._symbol_table
