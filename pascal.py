from nltk.grammar import Production


def print_corresponding_code(parse_result):
    tree = list(parse_result)[0]
    productions = list(tree.productions())
    for i in range(len(productions)):
        item: Production = productions[i]
        # print(i, ': ', item)
        if item.lhs().symbol() == 'declaracao_classe':
            # TODO: Accept more than 2 chracters in class name
            print('program ' + productions[i + 3].rhs()[0] + productions[i + 5].rhs()[0] + ';')
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
                tipo_dado = productions[i + 2].rhs()[0]
                # TODO: Support identificador with more than 1 letter
                identificador = productions[i + 5].rhs()[0]
                simbolo_atribuicao = ':='
                # TODO: Support valor with more than 1 digito
                valor = productions[i + 9].rhs()[0]
                simbolo_fim_instrucao = ';'
            else:
                # Declaração simples
                tipo_dado = productions[i + 2].rhs()[0]
                # TODO: Support identificador with more than 1 letter
                identificador = productions[i + 5].rhs()[0]
                simbolo_atribuicao = ''
                valor = ''
                simbolo_fim_instrucao = ';'
            # print(item.rhs())
            print('var')
            print(identificador + ': ' + tipo_dado + ' ' + simbolo_atribuicao + ' ' + valor + simbolo_fim_instrucao)
        if item.lhs().symbol() == 'declaracao_metodo':
            # Com retorno ou sem retorno?
            if productions[i + 2].lhs().symbol() == 'tipo_dado_sem_retorno':
                # TODO: Support identificador com mais de uma letra
                identificadorMetodo = productions[i + 5].rhs()[0]
                # TODO: Support method arguments
                print()
                print('procedure ' + identificadorMetodo + '();')
            else:
                print('function')
        if item.lhs().symbol() == 'atribuicao_variavel':
            # TODO: Support identificador com mais de uma letra
            identificadorVar = productions[i + 3].rhs()[0]
            # TODO: Support valor com mais de um digito
            valorVar = productions[i + 7].rhs()[0]
            print(identificadorVar + ' := ' + valorVar + ';')
