from Lexema import Lexema
from Identificador import Identificador
from prettytable import PrettyTable

# Palavras Reservadas
reserved_words = ['public', 'class', 'for', 'while', 'do', 'if', 'static', 'private', 'return']

# Tipos primitivos
primitive_types = ['int', 'char', 'double', 'float', 'void']

# Símbolos Especiais
symbols = ['+', ';', '-', '*', '/', '=', '==', '{', '}', '[', ']', '(', ')']

lexemas = []
identificadores = []

# Identificadores só aparecem depois de um tipo de dado ou depois da palavra class


def classify(word, line_number):
    if word != ' ' and word != '':
        if word in reserved_words:
            # print(word + ' é Palavra Reservada.')
            lexemas.append(Lexema(word, 'palavra reservada', line_number))
        elif word in primitive_types:
            # print(word + ' é Tipo Primitivo.')
            lexemas.append(Lexema(word, 'tipo primitivo', line_number))
        else:
            # print(word + ' não reconhecido')
            if lexemas[-1].token == 'class':
                lexemas.append(Lexema(word, 'Identificador', line_number))
                identificadores.append(Identificador(word, 'Classe'))
            elif lexemas[-1].token in primitive_types:
                lexemas.append(Lexema(word, 'Identificador', line_number))
                identificadores.append(Identificador(word, 'Variavel'))
            else:
                lexemas.append(Lexema(word, 'Não reconhecido', line_number))


lines = [line.rstrip('\n') for line in open('Exemplo1.java')]
current_line_number = 1
for line in lines:
    word = ''
    for char in line:
        if char in symbols:
            # print(char + ' é símbolo especial.')
            lexemas.append(Lexema(char, 'símbolo especial', current_line_number))
            word = ''
        elif char == ' ':
            classify(word, current_line_number)
            word = ''
        elif char.isdigit():
            char = str(char)
            word += char
        else:
            word += char
    current_line_number += 1

table_lexemas = PrettyTable(['Token', 'Classificação', 'Linha'])
for lexema in lexemas:
    table_lexemas.add_row([lexema.token, lexema.classification, str(lexema.line)])
print(table_lexemas)

table_identificadores = PrettyTable(['ID', 'Categ.'])
for identificador in identificadores:
    table_identificadores.add_row([identificador.id, identificador.categoria])
print(table_identificadores)
