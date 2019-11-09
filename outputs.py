from prettytable import PrettyTable


def print_lexema_table(lexemas: list):
    print()
    print("Tabela de Lexemas")
    table_lexemas = PrettyTable(['Token', 'Classificação', 'Linha'])
    for lexema in lexemas:
        table_lexemas.add_row([lexema.token, lexema.classification, str(lexema.line)])
    print(table_lexemas)


def print_symbol_table(identificadores: list):
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
