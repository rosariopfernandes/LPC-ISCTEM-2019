import file_operations
import lexical_analysis
import outputs
from lexeme_table import LexemeTable
from identifier_table import IdentifierTable
from pascal_converter import PascalConverter
from java_grammar import RESERVED_WORDS, PRIMITIVE_TYPES, SYMBOLS, CONTEXT_FREE_GRAMMAR


# Tabelas
_lexeme_table = LexemeTable()
_symbol_table = IdentifierTable()

is_parameter = False
parameter_count = 0
parameter_sequence = ''
variables_count = 1
last_type = ''
nivel = 0.0


def get_indentation(line: str):
    indentation = 0
    for char in line:
        if char == ' ':
            indentation += 1
        else:
            break
    return indentation


def verificar_valor():
    if _lexeme_table.get_last_token() == '=':
        indice_identificador = _symbol_table.index_of(_lexeme_table.get_second_last_token())
        if indice_identificador != -1:
            _symbol_table.update_value(indice_identificador, word)


def classify(word, line_number):
    global parameter_count, parameter_sequence, variables_count, last_type
    if word != ' ' and word != '':
        if word in RESERVED_WORDS:
            _lexeme_table.add_reserved_word(word, line_number)
        elif word in PRIMITIVE_TYPES:
            _lexeme_table.add_primitive_type(word, line_number)
            last_type = word
        else:
            if _lexeme_table.get_last_token() == 'class':
                _lexeme_table.add_identifier(word, line_number)
                _symbol_table.add_class(word, nivel)
            elif _lexeme_table.get_last_token() in PRIMITIVE_TYPES:
                if is_parameter:
                    _lexeme_table.add_identifier(word, line_number)
                    parameter_count += 1
                    parameter_sequence += _lexeme_table.get_second_last_token() + ', '
                    _symbol_table.add_parameter(word, _lexeme_table.get_second_last_token(), '-', '', nivel)
                else:
                    _lexeme_table.add_identifier(word, line_number)
                    _symbol_table.add_variable(word, _lexeme_table.get_second_last_token(), '-', '', nivel)
            elif _lexeme_table.get_last_token() == ',':
                # Várias variáveis na mesma linha
                variables_count += 1
                _symbol_table.add_variable(word, last_type, '-', '', nivel)
                _lexeme_table.add_identifier(word, line_number)
            elif word.isdigit():
                verificar_valor()
                _lexeme_table.add_numeric_constant(word, line_number)
            elif word == 'true' or word == 'false':
                verificar_valor()
                _lexeme_table.add_boolean_constant(word, line_number)
            elif word.startswith('\'') and word.endswith('\'') and len(word) == 3:
                # Verificar se esta constante está a ser atribuida à uma variável
                verificar_valor()
                _lexeme_table.add_char_constant(word, line_number)
            elif _symbol_table.contains(word):
                _lexeme_table.add_identifier(word, line_number)
            else:
                _lexeme_table.add_unknown(word, line_number)


lines = file_operations.read_lines_from_file('Ex.java')

if len(lines) == 0:
    exit()

current_line_number = 1

is_comentario = False

for line in lines:
    nivel = get_indentation(line) / 40
    # TODO: round this value
    if nivel > 0.0:
        nivel -= 0.1
    word = ''
    for char in line:
        # Verificar se o comentário termina nesta linha
        if line.find('*/') != -1:
            is_comentario = False
            break
        if is_comentario:
            # Ainda estamos em um comentário de várias linhas. Vamos saltar
            word = ''
            break
        if char == '*' and word == '/':
            # Comentário de várias linhas. Vamos procurar onde termina
            is_comentario = True
            word = ''
            # Verificar se termina na mesma linha
            if line.find('*/') != -1:
                is_comentario = False
            break
        if char == '/' and word == '/':
            # Comentário de uma linha. Vamos à próxima linha
            word = ''
            break
        if char in SYMBOLS:
            _lexeme_table.add_special_symbol(char, current_line_number)
            word = ''
        elif char == ' ' or char == ';' or char == ',':
            classify(word, current_line_number)
            if char == ';':
                variables_count = 0
                last_type = ''
            if char != ' ':
                _lexeme_table.add_special_symbol(char, current_line_number)
            word = ''
        elif char == '(' and _lexeme_table.get_last_token() in PRIMITIVE_TYPES:
            # Início de um método.
            _symbol_table.add_method(word, _lexeme_table.get_last_token(), parameter_count, parameter_sequence, '',
                                     nivel)
            _lexeme_table.add_identifier(word, current_line_number)
            _lexeme_table.add_special_symbol(char, current_line_number)
            # Vamos procurar parametros
            word = ''
            is_parameter = True
        elif char == '(' and (_lexeme_table.get_last_token() == 'if' or _lexeme_table.get_last_token() == 'while'):
            # Abriu uma estrutura de controlo
            _lexeme_table.add_special_symbol(char, current_line_number)
            word = ''
        elif char == ')':
            if _lexeme_table.get_last_token() in PRIMITIVE_TYPES:
                # Temos um parametro
                _symbol_table.add_parameter(word, _lexeme_table.get_last_token(), '', '', nivel)
                parameter_count += 1
                parameter_sequence += _lexeme_table.get_last_token()
                _lexeme_table.add_identifier(word, current_line_number)
                word = ''
            _lexeme_table.add_special_symbol(char, current_line_number)
            if parameter_sequence == '':
                parameter_sequence = '-'
            _symbol_table.update_params_sequence(-(parameter_count+1), parameter_sequence)
            _symbol_table.update_params_nr(-(parameter_count+1), parameter_count)
            parameter_sequence = ''
            parameter_count = 0
            is_parameter = False
            word = ''
        elif char.isdigit():
            char = str(char)
            word += char
        else:
            word += char
    current_line_number += 1

outputs.print_lexema_table(_lexeme_table.get_lexemes())

outputs.print_symbol_table(_symbol_table.get_identifiers())

# Declaração de variáveis do tipo primitivo (locais ou globais)
# instruções de atribuições simples
# Funções sem retorno
# Funções com retorno
# Estruturas de controlo (if e while)


parse_result = lexical_analysis.execute(_lexeme_table, CONTEXT_FREE_GRAMMAR)

if parse_result:
    PascalConverter().print_corresponding_code(parse_result)
