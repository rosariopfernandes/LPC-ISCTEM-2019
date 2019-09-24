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
variables_count = 1
last_type = ''


def index_of_identificador(identificador: str):
    for i in range(0, len(identificadores)):
        if identificadores[i].id == identificador:
            return i
    return -1


def is_identificador(word: str):
    for identificador in identificadores:
        if identificador.id == word:
            return True
    return False


def verificar_valor():
    if lexemas[-1].token == '=':
        indice_identificador = index_of_identificador(lexemas[-2].token)
        if indice_identificador != -1:
            identificadores[indice_identificador].valor = word


def classify(word, line_number):
    global parameter_count, parameter_sequence, variables_count, last_type
    if word != ' ' and word != '':
        if word in reserved_words:
            # print(word + ' é Palavra Reservada.')
            lexemas.append(Lexema(word, 'Palavra Reservada', line_number))
        elif word in primitive_types:
            # print(word + ' é Tipo Primitivo.')
            lexemas.append(Lexema(word, 'Tipo Primitivo', line_number))
            last_type = word
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
                    parameter_sequence += lexemas[-2].token + ', '
                else:
                    lexemas.append(Lexema(word, 'Identificador', line_number))
                    categoria = 'Variavel'
                    estrutura_memoria = 'Primitivo'
                    forma_passagem = 'Valor'
                    valor = '-'
                identificadores.append(Identificador(word, categoria, lexemas[-2].token, estrutura_memoria, valor, '-',
                                                     '-', forma_passagem, '', ''))
            elif lexemas[-1].token == ',':
                # Várias variáveis na mesma linha
                variables_count += 1
                identificadores.append(Identificador(word, 'Variavel', last_type, 'Primitivo', '-', '-',
                                                     '-', 'Valor', '', ''))
                lexemas.append(Lexema(word, 'Identificador', line_number))
            elif word.isdigit():
                verificar_valor()
                lexemas.append(Lexema(word, 'Constante numérica', line_number))
            elif word == 'true' or word == 'false':
                verificar_valor()
                lexemas.append(Lexema(word, 'Constante booleana', line_number))
            elif word.startswith('\'') and word.endswith('\'') and len(word) == 3:
                # Verificar se esta constante está a ser atribuida à uma variável
                verificar_valor()
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
            if char == ';':
                variables_count = 0
                last_type = ''
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
            if parameter_sequence == '':
                parameter_sequence = '-'
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
