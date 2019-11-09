from nltk.grammar import Production
from identifier_table import IdentifierTable

JAVA_PASCAL_MAPPING = {
    'byte': 'integer',
    'short': 'integer',
    'int': 'integer',
    'long': 'integer',
    'float': 'real',
    'double': 'real',
    'boolean': 'boolean',
    'char': 'char'
}


class PascalConverter(object):
    indentation: int

    def __init__(self):
        self.indentation = 0

    def _get_indentation(self):
        indentation_str = ''
        if self.indentation > 0:
            for i in range(0, self.indentation):
                indentation_str += ' '
        return indentation_str

    def print_corresponding_code(self, parse_result, symbols: list):
        _symbol_table_index = 0
        _global_variables = []
        _local_variables = []
        _output_lines = []
        _is_inside_method = False
        tree = list(parse_result)[0]
        productions = list(tree.productions())
        for i in range(len(productions)):
            item: Production = productions[i]
            # print(i, ': ', item)
            if item.lhs().symbol() == 'declaracao_classe':
                if symbols[_symbol_table_index].category == IdentifierTable.CATEGORY_CLASS:
                    _output_lines.append('program ' + symbols[_symbol_table_index].identifier + ';')
                    _symbol_table_index += 1
                else:
                    # TODO: Throw error
                    print('Declaração de classe não encontrada')
            if item.lhs().symbol() == 'inicio_bloco':
                _output_lines.append('begin')
                # TODO: Add 3 instead of assigning 3
                self.indentation = 3
            if item.lhs().symbol() == 'fim_bloco':
                # TODO: Check if its the last one
                if i == len(productions) - 1:
                    _output_lines.append('end.')
                else:
                    _output_lines.append('end;')
                    _is_inside_method = False
                _output_lines.append('')
                self.indentation = 0
            if item.lhs().symbol() == 'declaracao_variavel':
                identificador_variavel = symbols[_symbol_table_index].identifier
                tipo_dado_variavel = JAVA_PASCAL_MAPPING[symbols[_symbol_table_index].data_type]
                valor_variavel = symbols[_symbol_table_index].value
                if symbols[_symbol_table_index].category == IdentifierTable.CATEGORY_VARIABLE:
                    _symbol_table_index += 1
                else:
                    # TODO: Throw error
                    print('Esperava declaração de variável')
                if len(item.rhs()) == 5:
                    # Declaração com atribuição
                    simbolo_atribuicao = ':='
                    simbolo_fim_instrucao = ';'
                    declaracao_variavel = identificador_variavel + ': ' + tipo_dado_variavel \
                                          + ' ' + simbolo_atribuicao + ' ' + valor_variavel + simbolo_fim_instrucao
                else:
                    # Declaração simples
                    simbolo_fim_instrucao = ';'
                    declaracao_variavel = identificador_variavel + ': ' + \
                                          tipo_dado_variavel + simbolo_fim_instrucao
                if _is_inside_method:
                    _local_variables.append(declaracao_variavel)
                else:
                    _global_variables.append(declaracao_variavel)
            if item.lhs().symbol() == 'declaracao_metodo':
                _is_inside_method = True
                # Com retorno ou sem retorno?
                if productions[i + 2].lhs().symbol() == 'tipo_dado_sem_retorno':
                    identificador_metodo = symbols[_symbol_table_index].identifier
                    if symbols[_symbol_table_index].category == IdentifierTable.CATEGORY_METHOD:
                        _symbol_table_index += 1
                    else:
                        # TODO: Throw error
                        print('Esperava declaração de método')
                    # TODO: Support method arguments
                    _output_lines.append('')
                    _output_lines.append('procedure ' + identificador_metodo + '();')
                else:
                    _output_lines.append('function')
            if item.lhs().symbol() == 'atribuicao_variavel':
                # TODO: Support identificador com mais de uma letra
                identificadorVar = productions[i + 3].rhs()[0]
                # TODO: Support valor com mais de um digito
                valorVar = productions[i + 7].rhs()[0]
                _output_lines.append(self._get_indentation() + identificadorVar + ' := ' + valorVar + ';')

        # Primeiro imprime o nome do programa
        print(_output_lines[0])
        print()
        print('var')
        for variavel in _global_variables:
            print('   ' + variavel)
        print()
        for i in range(1, len(_output_lines)):
            print(_output_lines[i])
        for variavel in _local_variables:
            print(variavel)
