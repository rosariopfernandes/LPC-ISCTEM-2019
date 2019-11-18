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
from models.structure_if import StructureIf
from models.structure_while import StructureWhile


class JavaParser(object):

    def _parse_operand(self, productions: list, i: int):
        operando = ''
        tipo_operando = str(productions[i + 2].rhs()[0])
        if tipo_operando == 'identificador':
            operando = self._parse_identifier(productions, i + 2)
        elif tipo_operando == 'constante_inteira':
            # Get constante inteira
            j = i + 4
            while productions[j].lhs().symbol() == 'digito':
                lhs = str(productions[j].rhs()[0])
                operando += lhs
                j += 2
        else:
            j = i + 4
            while productions[j].lhs().symbol() != 'inicio_bloco' and\
                    productions[j].lhs().symbol() != 'operador_comparacao':
                if productions[j].lhs().symbol() != 'constante_inteira':
                    lhs = str(productions[j].rhs()[0])
                    operando += lhs
                j += 1
        return operando

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

    def _append_assignment(self, _current_function_declaration, _current_procedure_declaration,
                           _current_if_declaration, _current_while_declaration, assignment, _is_else):
        if _current_function_declaration is not None:
            if _current_if_declaration is not None:
                if _is_else:
                    _current_if_declaration.else_assignments.append(assignment)
                else:
                    _current_if_declaration.assignments.append(assignment)
            elif _current_while_declaration is not None:
                _current_while_declaration.assignments.append(assignment)
            else:
                _current_function_declaration.assignments.append(assignment)
        if _current_procedure_declaration is not None:
            if _current_if_declaration is not None:
                if _is_else:
                    _current_if_declaration.else_assignments.append(assignment)
                else:
                    _current_if_declaration.assignments.append(assignment)
            elif _current_while_declaration is not None:
                _current_while_declaration.assignments.append(assignment)
            else:
                _current_procedure_declaration.assignments.append(assignment)

    def get_class_declaration(self, parse_result, symbols: list, mapping: dict):
        _symbol_table_index = 0
        _is_inside_method = False
        _is_else = False
        _if_was_added = False
        _has_else = False
        _java_class = ClassDeclaration()
        _current_procedure_declaration: ProcedureDeclaration = None
        _current_function_declaration: FunctionDeclaration = None
        # TODO: Support nested ifs and whiles
        _current_if_declaration: StructureIf = None
        _current_while_declaration: StructureWhile = None

        # Verificar se existe alguma variável declarada 2 vezes
        for i in range(len(symbols)):
            symbol = symbols[i]
            for j in range(len(symbols)):
                if i == j:
                    continue
                another_symbol = symbols[j]
                if symbol.identifier == another_symbol.identifier and another_symbol.level >= symbol.level:
                    return None, {
                        'code': -1,
                        'message': 'Símbolo "' + symbol.identifier + '" já foi declarado.'
                    }

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
            # if item.lhs().symbol() == 'inicio_bloco':
            #     # _output_lines.append('begin')
            #     self.indentation = 3
            if item.lhs().symbol() == 'fim_bloco':
                if i != len(productions) - 1:
                    if _current_if_declaration is not None:
                        if not _if_was_added:
                            if _current_procedure_declaration is not None:
                                _current_procedure_declaration.assignments.append(_current_if_declaration)
                            if _current_function_declaration is not None:
                                _current_function_declaration.assignments.append(_current_if_declaration)
                            _if_was_added = True
                        if _has_else:
                            if _is_else:
                                _current_if_declaration = None
                                _is_else = False
                                _if_was_added = False
                        else:
                            _current_if_declaration = None
                            _is_else = False
                            _if_was_added = False
                    elif _current_while_declaration is not None:
                        if _current_procedure_declaration is not None:
                            _current_procedure_declaration.assignments.append(_current_while_declaration)
                        if _current_function_declaration is not None:
                            _current_function_declaration.assignments.append(_current_while_declaration)
                        _current_while_declaration = None
                    else:
                        if _current_procedure_declaration is not None:
                            _java_class.procedure_declarations.append(_current_procedure_declaration)
                            _current_procedure_declaration = None
                        if _current_function_declaration is not None:
                            _java_class.function_declarations.append(_current_function_declaration)
                            _current_function_declaration = None
                        _is_inside_method = False
                # self.indentation = 0
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
                    if str(item.rhs()[0]) == 'identificador':
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
                    elif str(productions[i + 1].rhs()[0]) == 'constante_inteira':
                        variable_name = ''
                        j = i + 3
                        while productions[j].lhs().symbol() == 'digito':
                            lhs = productions[j].rhs()[0]
                            variable_name += lhs
                            j += 2
                    elif str(productions[i + 1].rhs()[0]) == 'constante_booleana':
                        variable_name = productions[i + 3].rhs()[0]
                    elif str(productions[i + 1].rhs()[0]) == 'constante_real':
                        j = i + 3
                        variable_name = ''
                        while productions[j].lhs().symbol() != 'simbolo_fim_instrucao':
                            if productions[j].lhs().symbol() != 'constante_inteira':
                                lhs = str(productions[j].rhs()[0])
                                variable_name += lhs
                            j += 1
                    elif str(productions[i + 1].rhs()[0]) == 'constante_caracter':
                        if productions[i + 3].lhs().symbol() == 'caracter':
                            variable_name = "'" + str(productions[i + 4].rhs()[0]) + "'"
                        else:
                            variable_name = "'" + productions[i + 3].rhs()[0].symbol() + "'"
                    _current_function_declaration.return_value = variable_name
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
                self._append_assignment(_current_function_declaration, _current_procedure_declaration,
                                        _current_if_declaration, _current_while_declaration,
                                        MethodCall(method_name, _method_arguments), _is_else)
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
                    if productions[j + 1].lhs().symbol() == 'caracter':
                        variable_value = "'" + productions[j + 2].rhs()[0] + "'"
                    else:
                        variable_value = "'" + productions[j + 1].rhs()[0].symbol() + "'"
                self._append_assignment(_current_function_declaration, _current_procedure_declaration,
                                        _current_if_declaration, _current_while_declaration,
                                        VariableAssignment(variable_name, variable_value), _is_else)
            if item.lhs().symbol() == 'lista_parametros':
                # Verificar se tem parametros
                if len(productions[i].rhs()) > 0:
                    parameter_data_type = productions[i + 1].rhs()[0]
                    parameter_name = symbols[_symbol_table_index].identifier
                    _symbol_table_index += 1
                    self._append_assignment(_current_function_declaration, _current_procedure_declaration,
                                            _current_if_declaration, _current_while_declaration,
                                            VariableDeclaration(mapping[parameter_data_type], parameter_name), _is_else)
            if item.lhs().symbol() == 'estrutura_while':
                if str(productions[i+1].rhs()[0]) == 'identificador':
                    while_condition = self._parse_identifier(productions, i + 1)
                elif str(productions[i+1].rhs()[0]) == 'constante_booleana':
                    # Só colocou uma constante booleana
                    while_condition = str(productions[i+2].rhs()[0])
                else:
                    # Colocou operando1 operador operando2
                    # Obter operando1
                    while_condition = self._parse_operand(productions, i)

                    # Obter operador
                    j = i+1
                    while productions[j].lhs().symbol() != 'operador_comparacao':
                        j += 1
                    operador = productions[j].rhs()[0]
                    while_condition += ' ' + operador

                    # Obter operando2
                    while_condition += ' ' + self._parse_operand(productions, j-1)

                _current_while_declaration = StructureWhile()
                _current_while_declaration.condition = str(while_condition)
            if item.lhs().symbol() == 'estrutura_if':
                if len(item.rhs()) > 7:
                    _has_else = True
                else:
                    _has_else = False
                if str(productions[i+1].rhs()[0]) == 'identificador':
                    if_condition = self._parse_identifier(productions, i + 1)
                elif str(productions[i+1].rhs()[0]) == 'constante_booleana':
                    # Só colocou uma constante booleana
                    if_condition = str(productions[i+2].rhs()[0])
                else:
                    # Colocou operando1 operador operando2
                    # Obter operando1
                    if_condition = self._parse_operand(productions, i)

                    # Obter operador
                    j = i+1
                    while productions[j].lhs().symbol() != 'operador_comparacao':
                        j += 1
                    operador = productions[j].rhs()[0]
                    if_condition += ' ' + operador

                    # Obter operando2
                    if_condition += ' ' + self._parse_operand(productions, j-1)

                _current_if_declaration = StructureIf()
                _current_if_declaration.condition = str(if_condition)
            if item.lhs().symbol() == 'estrutura_else':
                _is_else = True

        return _java_class, _java_class.to_dict()
