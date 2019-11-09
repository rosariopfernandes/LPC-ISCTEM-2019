from lexeme_table import LexemeTable
from identificador import Identificador
import outputs
import lexical_analysis
import pascal
from java_grammar import RESERVED_WORDS, PRIMITIVE_TYPES, SYMBOLS, CONTEXT_FREE_GRAMMAR


# Tabelas
_lexeme_table = LexemeTable()
identificadores = []

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


def index_of_identificador(identificador: str):
    for i in range(0, len(identificadores)):
        if identificadores[i].identifier == identificador:
            return i
    return -1


def is_identificador(word: str):
    for identificador in identificadores:
        if identificador.identifier == word:
            return True
    return False


def verificar_valor():
    if _lexeme_table.get_last_token() == '=':
        indice_identificador = index_of_identificador(_lexeme_table.get_second_last_token())
        if indice_identificador != -1:
            identificadores[indice_identificador].value = word


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
                identificadores.append(Identificador(identifier=word, category='Classe', level=str(nivel)))
            elif _lexeme_table.get_last_token() in PRIMITIVE_TYPES:
                if is_parameter:
                    _lexeme_table.add_identifier(word, line_number)
                    categoria = 'Parametro'
                    estrutura_memoria = 'Primitivo'
                    forma_passagem = 'valor'
                    valor = '-'
                    parameter_count += 1
                    parameter_sequence += _lexeme_table.get_second_last_token() + ', '
                else:
                    _lexeme_table.add_identifier(word, line_number)
                    categoria = 'Variavel'
                    estrutura_memoria = 'Primitivo'
                    forma_passagem = 'Valor'
                    valor = '-'
                identificadores.append(Identificador(identifier=word, category=categoria,
                                                     data_type=_lexeme_table.get_second_last_token(),
                                                     memory_structure=estrutura_memoria, value=valor,
                                                     evaluation_strategy=forma_passagem, reference='',
                                                     level=str(nivel)))
            elif _lexeme_table.get_last_token() == ',':
                # Várias variáveis na mesma linha
                variables_count += 1
                identificadores.append(Identificador(identifier=word, category='Variavel', data_type=last_type,
                                                     memory_structure='Primitivo', value='Valor',
                                                     reference='', level=str(nivel)))
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
            elif is_identificador(word):
                _lexeme_table.add_identifier(word, line_number)
            else:
                _lexeme_table.add_unknown(word, line_number)


lines = [line.rstrip('\n') for line in open('Ex.java')]
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
            identificadores.append(Identificador(identifier=word, category='Método',
                                                 data_type=_lexeme_table.get_last_token(),
                                                 memory_structure='Primitivo', params_nr=parameter_count,
                                                 params_sequence=parameter_sequence, reference='', level=str(nivel)))
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
                identificadores.append(Identificador(identifier=word, category='Parametro',
                                                     data_type=_lexeme_table.get_last_token(),
                                                     memory_structure='Primitivo',
                                                     value='valor', reference='', level=str(nivel)))
                parameter_count += 1
                parameter_sequence += _lexeme_table.get_last_token()
                _lexeme_table.add_identifier(word, current_line_number)
                word = ''
            _lexeme_table.add_special_symbol(char, current_line_number)
            if parameter_sequence == '':
                parameter_sequence = '-'
            identificadores[-(parameter_count+1)].params_sequence = parameter_sequence
            identificadores[-(parameter_count+1)].params_nr = parameter_count
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

outputs.print_symbol_table(identificadores)

# Declaração de variáveis do tipo primitivo (locais ou globais)
# instruções de atribuições simples
# Funções sem retorno
# Funções com retorno
# Estruturas de controlo (if e while)


parse_result = lexical_analysis.execute(_lexeme_table, CONTEXT_FREE_GRAMMAR)

if parse_result:
    pascal.print_corresponding_code(parse_result)
