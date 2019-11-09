from nltk import ChartParser


def execute(lexeme_table, grammar):
    sentence = []
    for lexema in lexeme_table.get_lexemes():
        # Separar caracteres no caso de identificadores ou constantes
        if lexema.classification == 'Identificador' or (lexema.classification.startswith('Constante')):
            for char in lexema.token:
                sentence.append(char)
        else:
            sentence.append(lexema.token)
    parser = ChartParser(grammar)
    try:
        return parser.parse(sentence)
    except ValueError as e:
        print(e.args[0])
