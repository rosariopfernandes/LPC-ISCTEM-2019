from nltk import TopDownChartParser
from nltk import CFG


def execute(lexeme_table, grammar: CFG):
    sentence = []
    for lexema in lexeme_table.get_lexemes():
        # Separar caracteres no caso de identificadores ou constantes
        if lexema.classification == 'Identificador' or (lexema.classification.startswith('Constante')):
            for char in lexema.token:
                sentence.append(char)
        else:
            sentence.append(lexema.token)
    # grammar.check_coverage(sentence)
    parser = TopDownChartParser(grammar)
    try:
        result = parser.parse(sentence)
        return {
            'code': 200,
            'result': result
        }
    except ValueError as e:
        return {
            'code': -1,
            'message': e.args[0]
        }
