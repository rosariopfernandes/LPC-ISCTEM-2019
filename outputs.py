from prettytable import PrettyTable
from lexeme_table import LexemeTable
from identifier_table import IdentifierTable


def print_lexema_table(lexemas: LexemeTable):
    print()
    print("Tabela de Lexemas")
    table_lexemas = PrettyTable(['Token', 'Classificação', 'Linha'])
    for lexema in lexemas.get_lexemes():
        table_lexemas.add_row([lexema.token, lexema.classification, str(lexema.line)])
    print(table_lexemas)


def print_symbol_table(identificadores: IdentifierTable):
    print()
    print("Tabela de Símbolos")
    table_identificadores = PrettyTable(['ID', 'Categ.', 'Tipo', 'Estrut. Mem.', 'Valor', 'Nr Params', 'Seq. Params',
                                         'Forma de Passagem', 'Ref', 'Nível'])
    for identificador in identificadores.get_identifiers():
        table_identificadores.add_row([identificador.identifier, identificador.category, identificador.data_type,
                                       identificador.memory_structure, identificador.value, identificador.params_nr,
                                       identificador.params_sequence, identificador.evaluation_strategy,
                                       identificador.reference, identificador.level])
    print(table_identificadores)


def print_file_not_found():
    print('Ficheiro não encontrado')
