from nltk.grammar import Production
from nltk.grammar import Nonterminal
from nltk import Tree
from identifier_table import IdentifierTable
from models.class_declaration import ClassDeclaration
from models.procedure_declaration import ProcedureDeclaration
from models.function_declaration import FunctionDeclaration
from models.variable_assignment import VariableAssignment
from models.variable_declaration import VariableDeclaration
from models.method_call import MethodCall


class JavaParser(object):
    indentation: int

    def __init__(self):
        self.indentation = 0

    def _get_indentation(self):
        indentation_str = ''
        if self.indentation > 0:
            for i in range(0, self.indentation):
                indentation_str += ' '
        return indentation_str

    def _parse_identifier(self, productions, i):
        if len(productions[i + 1].rhs()) == 1:
            # identificador de 1 letra
            variable_name = productions[i + 3].rhs()[0]
        else:
            # identificador com mais de 1 letra
            # vamos formar o nome da variavel
            j = i + 3
            variable_name = ''
            while productions[j].lhs().symbol() == 'letra':
                lhs = productions[j].rhs()[0]
                variable_name += lhs
                j += 2
            j += 1
        return variable_name

    def get_class_declaration(self, parse_result, symbols: list, mapping: dict):
        _symbol_table_index = 0
        _is_inside_method = False
        _java_class = ClassDeclaration()
        _current_procedure_declaration: ProcedureDeclaration = None
        _current_function_declaration: FunctionDeclaration = None

        tree: Tree = list(parse_result)[0]
        # tree.pretty_print()
        productions = list(tree.productions())
        for i in range(len(productions)):
            item: Production = productions[i]
            print(i, ': ', item)
            if item.lhs().symbol() == 'declaracao_classe':
                if symbols[_symbol_table_index].category == IdentifierTable.CATEGORY_CLASS:
                    _java_class.class_name = symbols[_symbol_table_index].identifier
                    _symbol_table_index += 1
                else:
                    # TODO: Throw error
                    print('Declaração de classe não encontrada')
            if item.lhs().symbol() == 'inicio_bloco':
                # _output_lines.append('begin')
                # TODO: Add 3 instead of assigning 3
                self.indentation = 3
            if item.lhs().symbol() == 'fim_bloco':
                if i != len(productions) - 1:
                    # _output_lines.append('end;')
                    if _current_procedure_declaration is not None:
                        _java_class.procedure_declarations.append(_current_procedure_declaration)
                        _current_procedure_declaration = None
                    if _current_function_declaration is not None:
                        _java_class.function_declarations.append(_current_function_declaration)
                        _current_function_declaration = None
                    _is_inside_method = False
                self.indentation = 0
            if item.lhs().symbol() == 'declaracao_variavel':
                var_name = symbols[_symbol_table_index].identifier
                var_data_type = mapping[symbols[_symbol_table_index].data_type]
                var_value = ''
                j = i + 1
                # encontrar o valor da variavel
                while productions[j].lhs().symbol() != 'simbolo_fim_instrucao':
                    if productions[j].lhs().symbol() == 'digito' or productions[j].lhs().symbol() == 'separador':
                        lhs = productions[j].rhs()[0]
                        var_value += lhs
                    if productions[j].lhs().symbol() == 'constante_booleana':
                        var_value = productions[j].rhs()[0]
                        break
                    if productions[j].lhs().symbol() == 'constante_caracter':
                        if productions[j + 1].lhs().symbol() == 'caracter':
                            if type(productions[j + 1].rhs()[0]) == Nonterminal:
                                var_value = "'" + productions[j + 2].rhs()[0] + "'"
                            else:
                                var_value = "'" + productions[j + 1].rhs()[0] + "'"
                            break
                    j += 1
                if symbols[_symbol_table_index].category == IdentifierTable.CATEGORY_VARIABLE:
                    _symbol_table_index += 1
                else:
                    # TODO: Throw error
                    print('Esperava declaração de variável')
                if len(item.rhs()) == 5:
                    # Declaração com atribuição
                    var_declaration = VariableDeclaration(var_data_type, var_name, var_value)
                else:
                    # Declaração simples
                    var_declaration = VariableDeclaration(var_data_type, var_name)
                if _is_inside_method:
                    if _current_function_declaration is not None:
                        _current_function_declaration.local_declarations.append(var_declaration)
                    if _current_procedure_declaration is not None:
                        _current_procedure_declaration.local_declarations.append(var_declaration)
                else:
                    _java_class.variable_declarations.append(var_declaration)
            if item.lhs().symbol() == 'declaracao_metodo':
                _is_inside_method = True
                # Com retorno ou sem retorno?
                if productions[i + 1].lhs().symbol() == 'tipo_dado_sem_retorno':
                    identificador_metodo = symbols[_symbol_table_index].identifier
                    if symbols[_symbol_table_index].category == IdentifierTable.CATEGORY_METHOD:
                        _symbol_table_index += 1
                    else:
                        # TODO: Throw error
                        print('Esperava declaração de método')
                    # TODO: Support method arguments
                    _current_procedure_declaration = ProcedureDeclaration(identificador_metodo, [])
                else:
                    identificador_metodo = symbols[_symbol_table_index].identifier
                    if symbols[_symbol_table_index].category == IdentifierTable.CATEGORY_METHOD:
                        _symbol_table_index += 1
                    else:
                        # TODO: Throw error
                        print('Esperava declaração de método')
                    _current_function_declaration = FunctionDeclaration(mapping[productions[i + 1].rhs()[0]],
                                                                        identificador_metodo)
            if item.lhs().symbol() == 'retorno':
                if _current_function_declaration is not None:
                    # TODO: Support return of values
                    # TODO: Support return of identifiers with more than 1 letter
                    _current_function_declaration.return_value = productions[i+3].rhs()[0]
            if item.lhs().symbol() == 'chamada_metodo':
                method_name = self._parse_identifier(productions, i)
                _method_arguments = []
                j = i+1
                # Ir à lista de argumentos
                current_symbol = productions[j].lhs().symbol()
                while current_symbol != 'lista_argumentos':
                    j += 1
                    current_symbol = productions[j].lhs().symbol()
                _argument_name = ''
                # Pegar os argumentos
                while current_symbol != 'simbolo_fim_instrucao':
                    current_symbol = productions[j].lhs().symbol()
                    if current_symbol == 'letra':
                        _argument_name += productions[j].rhs()[0]
                    if current_symbol == 'simbolo_separador':
                        _method_arguments.append(_argument_name)
                        _argument_name = ''
                    j += 1
                # Pegar o último argumento
                if _argument_name != '':
                    _method_arguments.append(_argument_name)
                if _current_function_declaration is not None:
                    _current_function_declaration.assignments.append(MethodCall(method_name, _method_arguments))
                if _current_procedure_declaration is not None:
                    _current_procedure_declaration.assignments.append(MethodCall(method_name, _method_arguments))
            if item.lhs().symbol() == 'atribuicao_variavel':
                if len(productions[i + 1].rhs()) == 1:
                    # identificador de 1 letra
                    variable_name = productions[i + 3].rhs()[0]
                    j = i + 6
                else:
                    # identificador com mais de 1 letra
                    # vamos formar o nome da variavel
                    j = i + 3
                    variable_name = ''
                    while productions[j].lhs().symbol() == 'letra':
                        lhs = productions[j].rhs()[0]
                        variable_name += lhs
                        j += 2
                    j += 1
                variable_value = ''
                if productions[j].lhs().symbol() == 'constante_inteira':
                    variable_value = ''
                    j += 1
                    while productions[j].lhs().symbol() == 'digito':
                        lhs = productions[j].rhs()[0]
                        variable_value += lhs
                        j += 2
                if productions[j].lhs().symbol() == 'constante_booleana':
                    variable_value = productions[j].rhs()[0]
                if productions[j].lhs().symbol() == 'constante_real':
                    j += 1
                    while productions[j].lhs().symbol() != 'simbolo_fim_instrucao':
                        if productions[j].lhs().symbol() != 'constante_inteira':
                            lhs = productions[j].rhs()[0]
                            variable_value += lhs
                        j += 1
                if productions[j].lhs().symbol() == 'constante_caracter':
                    print('test ', productions[j + 1].lhs().symbol())
                    if productions[j + 1].lhs().symbol() == 'caracter':
                        variable_value = "'" + productions[j + 2].rhs()[0] + "'"
                    else:
                        variable_value = "'" + productions[j + 1].rhs()[0].symbol() + "'"
                if _current_procedure_declaration is not None:
                    _current_procedure_declaration.assignments.append(VariableAssignment(variable_name, variable_value))
                if _current_function_declaration is not None:
                    _current_function_declaration.assignments.append(VariableAssignment(variable_name, variable_value))
            if item.lhs().symbol() == 'lista_parametros':
                # Verificar se tem parametros
                if len(productions[i].rhs()) > 0:
                    parameter_data_type = productions[i + 1].rhs()[0]
                    parameter_name = symbols[_symbol_table_index].identifier
                    _symbol_table_index += 1
                    if _current_procedure_declaration is not None:
                        _current_procedure_declaration.arguments.append(
                            VariableDeclaration(mapping[parameter_data_type], parameter_name))
                    if _current_function_declaration is not None:
                        _current_function_declaration.arguments.append(
                            VariableDeclaration(mapping[parameter_data_type], parameter_name))

        return _java_class
