from Lexema import Lexema
from Identificador import Identificador
from prettytable import PrettyTable

# Palavras Reservadas
reserved_words = ['public', 'class', 'for', 'while', 'do', 'if', 'static', 'private', 'return']

# Tipos primitivos
primitive_types = ['int', 'char', 'double', 'float', 'void', 'boolean', 'short', 'long']

# Símbolos Especiais
# TODO: classificar divisão (/) tem conflito com comentário de uma linha
symbols = ['+', '-', '*', '=', '{', '}', '[', ']']

lexemas = []
identificadores = []
is_parameter = False
parameter_count = 0
parameter_sequence = ''

# Identificadores só aparecem depois de um tipo de dado ou depois da palavra class


def is_identificador(word: str):
    for identificador in identificadores:
        if identificador.id == word:
            return True
    return False


def classify(word, line_number):
    global parameter_count, parameter_sequence
    if word != ' ' and word != '':
        if word in reserved_words:
            # print(word + ' é Palavra Reservada.')
            lexemas.append(Lexema(word, 'Palavra Reservada', line_number))
        elif word in primitive_types:
            # print(word + ' é Tipo Primitivo.')
            lexemas.append(Lexema(word, 'Tipo Primitivo', line_number))
        else:
            if lexemas[-1].token == 'class':
                lexemas.append(Lexema(word, 'Identificador', line_number))
                identificadores.append(Identificador(word, 'Classe', '-', '-', '-', '-', '-', '-', '-', '-'))
            elif lexemas[-1].token in primitive_types:
                if is_parameter:
                    lexemas.append(Lexema(word, 'Identificador', line_number))
                    categoria = 'Parametro'
                    estrutura_memoria = 'Primitivo'
                    forma_passagem = 'valor'
                    valor = '-'
                    parameter_count += 1
                    parameter_sequence += lexemas[-1].token + ', '
                else:
                    lexemas.append(Lexema(word, 'Identificador', line_number))
                    categoria = 'Variavel'
                    estrutura_memoria = 'Primitivo'
                    forma_passagem = 'valor'
                    valor = ''
                identificadores.append(Identificador(word, categoria, lexemas[-1].token, estrutura_memoria, valor, '-',
                                                     '-', forma_passagem, '', ''))
            elif word.isdigit():
                lexemas.append(Lexema(word, 'Constante numérica', line_number))
            elif word == 'true' or word == 'false':
                lexemas.append(Lexema(word, 'Constante booleana', line_number))
            elif word.startswith('\'') and word.endswith('\'') and len(word) == 3:
                lexemas.append(Lexema(word, 'Constante caracter', line_number))
            elif is_identificador(word):
                lexemas.append(Lexema(word, 'Identificador', line_number))
            else:
                lexemas.append(Lexema(word, 'Não reconhecido', line_number))


lines = [line.rstrip('\n') for line in open('Exemplo1.java')]
current_line_number = 1
for line in lines:
    word = ''
    for char in line:

        if char == '/' and word == '/':
            # Comentário de uma linha. Vamos à próxima linha
            word = ''
            break
        if char in symbols:
            lexemas.append(Lexema(char, 'Símbolo especial', current_line_number))
            word = ''
        elif char == ' ' or char == ';' or char == ',':
            classify(word, current_line_number)
            if char != ' ':
                lexemas.append(Lexema(char, 'Símbolo especial', current_line_number))
            word = ''
        elif char == '(' and lexemas[-1].token in primitive_types:
            # Início de um método.
            identificadores.append(Identificador(word, 'Método', lexemas[-1].token, 'Primitivo', '-', parameter_count,
                                                 parameter_sequence, '-', '', ''))
            lexemas.append(Lexema(word, 'Identificador', current_line_number))
            lexemas.append(Lexema(char, 'Símbolo especial', current_line_number))
            # Vamos procurar parametros
            word = ''
            is_parameter = True
        elif char == ')':
            if lexemas[-1].token in primitive_types:
                # Temos um parametro
                identificadores.append(Identificador(word, 'Parametro', lexemas[-1].token, 'Primitivo', '-',
                                                     '-', '-', 'valor', '', ''))
                parameter_count += 1
                parameter_sequence += lexemas[-1].token
                lexemas.append(Lexema(word, 'Identificador', current_line_number))
                word = ''
            lexemas.append(Lexema(char, 'Símbolo especial', current_line_number))
            identificadores[-(parameter_count+1)].seq_params = parameter_sequence
            identificadores[-(parameter_count+1)].nr_params = parameter_count
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

print()
print("Tabela de Lexemas")
table_lexemas = PrettyTable(['Token', 'Classificação', 'Linha'])
for lexema in lexemas:
    table_lexemas.add_row([lexema.token, lexema.classification, str(lexema.line)])
print(table_lexemas)

print()
print("Tabela de Símbolos")
table_identificadores = PrettyTable(['ID', 'Categ.', 'Tipo', 'Estrut. Mem.', 'Valor', 'Nr Params', 'Seq. Params',
                                     'Forma de Passagem', 'Ref', 'Nível'])
for identificador in identificadores:
    table_identificadores.add_row([identificador.id, identificador.categoria, identificador.tipo,
                                   identificador.estrutura_memoria, identificador.valor, identificador.nr_params,
                                   identificador.seq_params, identificador.forma_passagem, identificador.ref,
                                   identificador.nivel])
print(table_identificadores)
