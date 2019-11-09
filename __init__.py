from Lexema import Lexema
from Identificador import Identificador
from prettytable import PrettyTable
import nltk
from nltk.grammar import Production

# Palavras Reservadas
reserved_words = ['public', 'class', 'for', 'while', 'if', 'static', 'private', 'return']

# Tipos primitivos
primitive_types = ['int', 'char', 'double', 'float', 'void', 'boolean', 'short', 'long']

# Símbolos Especiais
# TODO: classificar multiplicacao(*) e divisão (/). Tem conflito com comentários
symbols = ['+', '-', '=', '{', '}', '[', ']']

lexemas = []
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
                identificadores.append(Identificador(word, 'Classe', '-', '-', '-', '-', '-', '-', '-', str(nivel)))
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
                                                     '-', forma_passagem, '', str(nivel)))
            elif lexemas[-1].token == ',':
                # Várias variáveis na mesma linha
                variables_count += 1
                identificadores.append(Identificador(word, 'Variavel', last_type, 'Primitivo', '-', '-',
                                                     '-', 'Valor', '', str(nivel)))
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
                                                 parameter_sequence, '-', '', str(nivel)))
            lexemas.append(Lexema(word, 'Identificador', current_line_number))
            lexemas.append(Lexema(char, 'Símbolo especial', current_line_number))
            # Vamos procurar parametros
            word = ''
            is_parameter = True
        elif char == '(' and (lexemas[-1].token == 'if' or lexemas[-1].token == 'while'):
            # Abriu uma estrutura de controlo
            lexemas.append(Lexema(char, 'Símbolo especial', current_line_number))
            # Vamos procurar parametros
            word = ''
        elif char == ')':
            if lexemas[-1].token in primitive_types:
                # Temos um parametro
                identificadores.append(Identificador(word, 'Parametro', lexemas[-1].token, 'Primitivo', '-',
                                                     '-', '-', 'valor', '', str(nivel)))
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

# Declaração de variáveis do tipo primitivo (locais ou globais)
# instruções de atribuições simples
# Funções sem retorno
# Funções com retorno
# Estruturas de controlo (if e while)

test_grammar = nltk.CFG.fromstring(
    """
    declaracao_classe -> "public" "class" identificador inicio_bloco corpo_classe fim_bloco
    
    corpo_classe -> declaracao_variavel
    corpo_classe -> declaracao_metodo
    corpo_classe -> corpo_classe declaracao_variavel
    corpo_classe -> corpo_classe declaracao_metodo

    declaracao_metodo -> tipo_dado identificador '(' ')' inicio_bloco corpo_metodo fim_bloco
    
    corpo_metodo -> 
    corpo_metodo -> declaracao_variavel
    corpo_metodo -> atribuicao_variavel
    corpo_metodo -> chamada_metodo
    corpo_metodo -> corpo_metodo declaracao_variavel
    corpo_metodo -> corpo_metodo atribuicao_variavel
    corpo_metodo -> corpo_metodo chamada_metodo

    declaracao_variavel -> tipo_dado identificador simbolo_fim_instrucao
    declaracao_variavel -> tipo_dado identificador simbolo_atribuicao valor simbolo_fim_instrucao
    
    atribuicao_variavel -> identificador simbolo_atribuicao valor simbolo_fim_instrucao
    
    tipo_dado -> tipo_dado_com_retorno | tipo_dado_sem_retorno
    tipo_dado_com_retorno -> "int" | "char" | "byte" | "long" | "short" | "boolean"
    tipo_dado_sem_retorno -> "void"
    
    chamada_metodo -> identificador '(' ')' simbolo_fim_instrucao
    
    inicio_bloco -> '{'
    simbolo_separador -> ','
    simbolo_atribuicao -> '='
    simbolo_fim_instrucao -> ';'
    fim_bloco -> '}'

    identificador -> inicio_identificador
    identificador -> inicio_identificador corpo_identificador
    inicio_identificador -> '_' | letra
    corpo_identificador -> '_' | letra | constante_inteira
    corpo_identificador -> corpo_identificador palavra
    
    palavra -> letra
    palavra -> palavra letra
    letra -> 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
    letra -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
    
    valor -> constante_inteira
    
    constante_inteira -> digito
    constante_inteira -> constante_inteira digito
    digito -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    """
)


def analyzeLexemas():
    sentence = []
    for lexema in lexemas:
        # Separar caracteres no caso de identificadores ou constantes
        if lexema.classification == 'Identificador' or (lexema.classification.startswith('Constante')):
            for char in lexema.token:
                sentence.append(char)
        else:
            sentence.append(lexema.token)
    parser = nltk.ChartParser(test_grammar)
    parse_result = parser.parse(sentence)

    tree = list(parse_result)[0]
    productions = list(tree.productions())
    for i in range(len(productions)):
        item: Production = productions[i]
        # print(i, ': ', item)
        if item.lhs().symbol() == 'declaracao_classe':
            # TODO: Accept more than 2 chracters in class name
            print('program ' + productions[i+3].rhs()[0] + productions[i+5].rhs()[0] + ';')
            print()
            # ntIdentificador: Nonterminal = item.rhs()[2]
            # print(item.rhs())
            # print(type(item.rhs()[2]))
        if item.lhs().symbol() == 'inicio_bloco':
            print('begin')
        if item.lhs().symbol() == 'fim_bloco':
            # TODO: Check if its the last one
            if i == len(productions) - 1:
                print('end.')
            else:
                print('end;')
            print()
        if item.lhs().symbol() == 'declaracao_variavel':
            if len(item.rhs()) == 5:
                # Declaração com atribuição
                tipo_dado = productions[i+2].rhs()[0]
                # TODO: Support identificador with more than 1 letter
                identificador = productions[i+5].rhs()[0]
                simbolo_atribuicao = ':='
                # TODO: Support valor with more than 1 digito
                valor = productions[i+9].rhs()[0]
                simbolo_fim_instrucao = ';'
            else:
                # Declaração simples
                tipo_dado = productions[i+2].rhs()[0]
                # TODO: Support identificador with more than 1 letter
                identificador = productions[i+5].rhs()[0]
                simbolo_atribuicao = ''
                valor = ''
                simbolo_fim_instrucao = ';'
            # print(item.rhs())
            print('var')
            print(identificador + ': ' + tipo_dado + ' ' + simbolo_atribuicao + ' ' + valor + simbolo_fim_instrucao)
        if item.lhs().symbol() == 'declaracao_metodo':
            # Com retorno ou sem retorno?
            if productions[i+2].lhs().symbol() == 'tipo_dado_sem_retorno':
                # TODO: Support identificador com mais de uma letra
                identificadorMetodo = productions[i+5].rhs()[0]
                # TODO: Support method arguments
                print()
                print('procedure ' + identificadorMetodo + '();')
            else:
                print('function')
        if item.lhs().symbol() == 'atribuicao_variavel':
            # TODO: Support identificador com mais de uma letra
            identificadorVar = productions[i+3].rhs()[0]
            # TODO: Support valor com mais de um digito
            valorVar = productions[i+7].rhs()[0]
            print(identificadorVar + ' := ' + valorVar + ';')


analyzeLexemas()
