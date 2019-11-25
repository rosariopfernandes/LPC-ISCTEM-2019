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


class SemanticAnalysis(object):

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
            while productions[j].lhs().symbol() != 'inicio_bloco' and \
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

    def get_class_declaration(self, parse_result, lexemes: list, mapping: dict):
        _is_inside_method = False
        _is_else = False
        _if_was_added = False
        _has_else = False
        _level = 0.0
        _java_class = ClassDeclaration()
        _current_procedure_declaration: ProcedureDeclaration = None
        _current_function_declaration: FunctionDeclaration = None
        # TODO: Support nested ifs and whiles
        _current_if_declaration: StructureIf = None
        _current_while_declaration: StructureWhile = None

        _symbol_table = IdentifierTable()

        tree: Tree = list(parse_result)[0]
        # tree.draw()
        productions = list(tree.productions())
        for i in range(len(productions)):
            item: Production = productions[i]
            print(i, ': ', item)
            if item.lhs().symbol() == 'declaracao_classe':
                nome_class = self._parse_identifier(productions, i+1)
                _java_class.class_name = nome_class
                _symbol_table.add_class(nome_class, _level)
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
                        _level -= 0.1
                        if _current_procedure_declaration is not None:
                            _param_count = 0
                            _param_seq = '-'
                            for param in _current_procedure_declaration.arguments:
                                _param_seq += param + ', '
                                _param_count += 1
                            if _param_seq != '-':
                                _param_seq = _param_seq[:-2]
                            method_name = _current_procedure_declaration.procedure_name
                            if _symbol_table.has_been_declared(method_name, _level):
                                return None, {
                                    'code': -1,
                                    'message': 'Símbolo ' + method_name + ' já foi declarado.'
                                }, _symbol_table.to_dict()
                            _symbol_table.add_method(_current_procedure_declaration.procedure_name,
                                                     'void', _param_count, _param_seq, 'refMethod', _level)
                            _java_class.procedure_declarations.append(_current_procedure_declaration)
                            _current_procedure_declaration = None
                        if _current_function_declaration is not None:
                            _param_count = 0
                            _param_seq = '-'
                            for param in _current_function_declaration.arguments:
                                _param_seq += param + ', '
                                _param_count += 1
                            if _param_seq != '-':
                                _param_seq = _param_seq[:-2]
                            method_name = _current_function_declaration.function_name
                            if _symbol_table.has_been_declared(method_name, _level):
                                return None, {
                                    'code': -1,
                                    'message': 'Símbolo ' + method_name + ' já foi declarado.'
                                }, _symbol_table.to_dict()
                            _symbol_table.add_method(_current_function_declaration.function_name,
                                                     _current_function_declaration.data_type,
                                                     _param_count, _param_seq, 'refMethod', _level)
                            _java_class.function_declarations.append(_current_function_declaration)
                            _current_function_declaration = None
                        _is_inside_method = False
                # self.indentation = 0
            if item.lhs().symbol() == 'declaracao_variavel':
                j = i + 1

                pos_attrib = 2
                if str(item.rhs()[0]) == 'modificador':
                    j += 1
                    pos_attrib += 1

                var_name = self._parse_identifier(productions, j)
                java_data_type = str(productions[j].rhs()[0])
                var_data_type = mapping[java_data_type]
                var_value = ''

                if str(item.rhs()[pos_attrib]) == 'simbolo_atribuicao':
                    tipo_constante = productions[j].lhs().symbol()
                    l = j
                    while tipo_constante != 'valor':
                        l += 1
                        tipo_constante = productions[l].lhs().symbol()
                    tipo_constante = str(productions[l].rhs()[0])

                    # encontrar o valor da variavel
                    while productions[j].lhs().symbol() != 'simbolo_fim_instrucao':
                        if productions[j].lhs().symbol() == 'digito' or productions[j].lhs().symbol() == 'separador':
                            lhs = productions[j].rhs()[0]
                            var_value += lhs
                        if productions[j].lhs().symbol() == 'constante_booleana':
                            var_value = productions[j].rhs()[0]
                            if java_data_type != 'boolean':
                                error_line = 0
                                for k in range(len(lexemes)):
                                    if lexemes[k].token == var_name and lexemes[k + 1].token == '=' and \
                                            lexemes[k + 2].token == var_value:
                                        error_line = lexemes[k].line
                                        break
                                return None, {
                                    'code': -1,
                                    'message': 'Variável "' + var_name + '" do tipo ' + java_data_type +
                                               ' não pode receber valor ' + var_value,
                                    'line': error_line
                                }, _symbol_table.to_dict()
                            break
                        if productions[j].lhs().symbol() == 'constante_caracter':
                            if productions[j + 1].lhs().symbol() == 'caracter':
                                if type(productions[j + 1].rhs()[0]) == Nonterminal:
                                    var_value = "'" + productions[j + 2].rhs()[0] + "'"
                                else:
                                    var_value = "'" + productions[j + 1].rhs()[0] + "'"
                                if java_data_type != 'char':
                                    error_line = 0
                                    for k in range(len(lexemes)):
                                        if lexemes[k].token == var_name and lexemes[k + 1].token == '=' and \
                                                lexemes[k + 2].token == var_value:
                                            error_line = lexemes[k].line
                                            break
                                    return None, {
                                        'code': -1,
                                        'message': 'Variável "' + var_name + '" do tipo ' + java_data_type +
                                                   ' não pode receber valor ' + var_value,
                                        'line': error_line
                                    }, _symbol_table.to_dict()
                                break
                        j += 1
                    if tipo_constante == 'constante_inteira':
                        if java_data_type != 'int' and java_data_type != 'short' and java_data_type != 'byte' \
                                and java_data_type != 'long':
                            error_line = 0
                            for k in range(len(lexemes)):
                                if lexemes[k].token == var_name and lexemes[k + 1].token == '=' and \
                                        lexemes[k + 2].token == var_value:
                                    print(error_line)
                                    error_line = lexemes[k].line
                                    break
                            return None, {
                                'code': -1,
                                'message': 'Variável "' + var_name + '" do tipo ' + java_data_type +
                                           ' não pode receber valor ' + var_value,
                                'line': error_line
                            }, _symbol_table.to_dict()
                    elif tipo_constante == 'constante_real':
                        if java_data_type != 'float' and java_data_type != 'double':
                            error_line = 0
                            for k in range(len(lexemes)):
                                if lexemes[k].token == var_name and lexemes[k + 1].token == '=' and \
                                        lexemes[k + 2].token == var_value:
                                    print(error_line)
                                    error_line = lexemes[k].line
                                    break
                            return None, {
                                'code': -1,
                                'message': 'Variável "' + var_name + '" do tipo ' + java_data_type +
                                           ' não pode receber valor ' + var_value,
                                'line': error_line
                            }, _symbol_table.to_dict()
                    # Declaração com atribuição
                    var_declaration = VariableDeclaration(var_data_type, var_name, var_value)
                    if _symbol_table.has_been_declared(var_name, _level):
                        return None, {
                            'code': -1,
                            'message': 'Símbolo "' + var_name + '" já foi declarado.'
                        }, _symbol_table.to_dict()
                    _symbol_table.add_variable(var_name, java_data_type, var_value, 'ref', _level)
                else:
                    # Declaração simples
                    var_declaration = VariableDeclaration(var_data_type, var_name)
                    if _symbol_table.has_been_declared(var_name, _level):
                        return None, {
                            'code': -1,
                            'message': 'Símbolo "' + var_name + '" já foi declarado.'
                        }, _symbol_table.to_dict()
                    _symbol_table.add_variable(var_name, java_data_type, '-', 'ref', _level)
                if _is_inside_method:
                    if _current_function_declaration is not None:
                        _current_function_declaration.local_declarations.append(var_declaration)
                    if _current_procedure_declaration is not None:
                        _current_procedure_declaration.local_declarations.append(var_declaration)
                else:
                    _java_class.variable_declarations.append(var_declaration)
            if item.lhs().symbol() == 'declaracao_metodo':
                _is_inside_method = True
                _level += 0.1
                j = i + 1
                pos_attrib = 0
                # Verificar se tem modificador de visibilidade
                if str(item.rhs()[0]) == 'modificador':
                    j += 1
                    pos_attrib += 2
                identificador_metodo = self._parse_identifier(productions, j)
                # Com retorno ou sem retorno?
                if productions[j].lhs().symbol() == 'tipo_dado_sem_retorno':
                    # TODO: Support method arguments
                    _current_procedure_declaration = ProcedureDeclaration(identificador_metodo, [])
                else:
                    _current_function_declaration = FunctionDeclaration(mapping[str(productions[j].rhs()[pos_attrib])],
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
                j = i + 1
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
                if not _symbol_table.has_been_declared(variable_name, _level):
                    return None, {
                        'code': -1,
                        'message': 'Variável ' + variable_name + ' não foi declarada.'
                    }, _symbol_table.to_dict()
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
                # TODO: Check if this really works
                if len(productions[i].rhs()) > 0:
                    parameter_data_type = productions[i + 1].rhs()[0]
                    parameter_name = self._parse_identifier(productions, i + 1)
                    # TODO: Add parameter after method
                    _symbol_table.add_parameter(parameter_name, parameter_data_type, '-', 'r', _level)
                    self._append_assignment(_current_function_declaration, _current_procedure_declaration,
                                            _current_if_declaration, _current_while_declaration,
                                            VariableDeclaration(mapping[parameter_data_type], parameter_name), _is_else)
            if item.lhs().symbol() == 'estrutura_while':
                if str(productions[i + 1].rhs()[0]) == 'identificador':
                    while_condition = self._parse_identifier(productions, i + 1)
                elif str(productions[i + 1].rhs()[0]) == 'constante_booleana':
                    # Só colocou uma constante booleana
                    while_condition = str(productions[i + 2].rhs()[0])
                else:
                    # Colocou operando1 operador operando2
                    # Obter operando1
                    while_condition = self._parse_operand(productions, i)

                    # Obter operador
                    j = i + 1
                    while productions[j].lhs().symbol() != 'operador_comparacao':
                        j += 1
                    operador = productions[j].rhs()[0]
                    if len(productions[j].rhs()) > 1:
                        if operador != '=':
                            operador += str(productions[j].rhs()[1])
                    while_condition += ' ' + operador

                    # Obter operando2
                    while_condition += ' ' + self._parse_operand(productions, j - 1)

                _current_while_declaration = StructureWhile()
                _current_while_declaration.condition = str(while_condition)
            if item.lhs().symbol() == 'estrutura_if':
                if len(item.rhs()) > 7:
                    _has_else = True
                else:
                    _has_else = False
                if str(productions[i + 1].rhs()[0]) == 'identificador':
                    if_condition = self._parse_identifier(productions, i + 1)
                elif str(productions[i + 1].rhs()[0]) == 'constante_booleana':
                    # Só colocou uma constante booleana
                    if_condition = str(productions[i + 2].rhs()[0])
                else:
                    # Colocou operando1 operador operando2
                    # Obter operando1
                    if_condition = self._parse_operand(productions, i)

                    # Obter operador
                    j = i + 1
                    while productions[j].lhs().symbol() != 'operador_comparacao':
                        j += 1
                    operador = productions[j].rhs()[0]
                    if len(productions[j].rhs()) > 1:
                        if operador != '=':
                            operador += str(productions[j].rhs()[1])
                    if_condition += ' ' + operador

                    # Obter operando2
                    if_condition += ' ' + self._parse_operand(productions, j - 1)

                _current_if_declaration = StructureIf()
                _current_if_declaration.condition = str(if_condition)
            if item.lhs().symbol() == 'estrutura_else':
                _is_else = True

        return _java_class, _java_class.to_dict(), _symbol_table.to_dict()
