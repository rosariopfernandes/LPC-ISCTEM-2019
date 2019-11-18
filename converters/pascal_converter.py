from models.class_declaration import ClassDeclaration
from models.variable_assignment import VariableAssignment
from models.method_call import MethodCall
from models.structure_if import StructureIf
from models.structure_while import StructureWhile

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


def _get_passed_arguments(method):
    passed_arguments = ''
    for argument in method.arguments:
        passed_arguments += argument + ', '
    if len(passed_arguments) > 0:
        passed_arguments = passed_arguments[:-2]
    return passed_arguments


def _get_arguments(method):
    procedure_arguments = ''
    for argument in method.arguments:
        procedure_arguments += argument.variable_name + ': ' + argument.data_type + ', '
    if len(procedure_arguments) > 0:
        procedure_arguments = procedure_arguments[:-2]
    return procedure_arguments


def _append_local_declarations(method, lines):
    if len(method.local_declarations) > 0:
        lines.append('var')
    for declaration in method.local_declarations:
        declaration_output = '   ' + declaration.variable_name + ': ' + declaration.data_type
        if declaration.value is not None:
            declaration_output += ' := ' + declaration.value
        lines.append(declaration_output + ';')


def _get_indentation(indentation: int):
    spaces = ''
    for i in range(indentation):
        spaces += ' '
    return spaces


def _append_assignments(indentation: int, method, lines, is_else=False):
    _assignments = method.assignments
    if is_else:
        _assignments = method.else_assignments
    for assignment in _assignments:
        print(assignment.to_dict())
        if type(assignment) == VariableAssignment:
            # Atribuição de variáveis
            lines.append(_get_indentation(indentation) + assignment.variable_name + ' := ' + assignment.value + ';')
        elif type(assignment) == MethodCall:
            # Chamada de métodos
            lines.append(_get_indentation(indentation) + assignment.method_name + '(' + _get_passed_arguments(assignment) + ');')
        elif type(assignment) == StructureIf:
            # Estructura if
            lines.append(_get_indentation(indentation) + 'if ( ' + assignment.condition + ' ) then')
            lines.append(_get_indentation(indentation) + 'begin')
            _append_assignments(indentation + 3, assignment, lines)
            lines.append(_get_indentation(indentation) + 'end;')
            if len(assignment.else_assignments) > 0:
                lines.append(_get_indentation(indentation) + 'else')
                lines.append(_get_indentation(indentation) + 'begin')
                _append_assignments(indentation + 3, assignment, lines, True)
                lines.append(_get_indentation(indentation) + 'end;')
            lines.append(_get_indentation(indentation))
        elif type(assignment) == StructureWhile:
            lines.append(_get_indentation(indentation) + 'while ( ' + assignment.condition + ' ) do')
            lines.append(_get_indentation(indentation) + 'begin')
            _append_assignments(indentation + 3, assignment, lines)
            lines.append(_get_indentation(indentation) + 'end;')
            lines.append(_get_indentation(indentation))


def get_pascal_equivalent(_java_class: ClassDeclaration):
    indentation = 3
    # Nome do programa
    pascal_lines = ['program ' + _java_class.class_name + ';', '']

    # Imprime variáveis globais
    if len(_java_class.variable_declarations) > 0:
        pascal_lines.append('var')
    for variavel in _java_class.variable_declarations:
        declaration_output = '   ' + variavel.variable_name + ': ' + variavel.data_type
        if variavel.value is not None:
            declaration_output += ' := ' + variavel.value
        pascal_lines.append(declaration_output + ';')
    pascal_lines.append('')

    # Imprime Functions
    for _function in _java_class.function_declarations:
        function_arguments = _get_arguments(_function)
        pascal_lines.append('function ' + _function.function_name + '(' + function_arguments + '): ' + _function.data_type + ';')
        _append_local_declarations(_function, pascal_lines)
        pascal_lines.append('begin')
        _append_assignments(indentation, _function, pascal_lines)
        # Imprimir o retorno:
        pascal_lines.append('   ' + _function.function_name + ' := ' + _function.return_value + ';')
        pascal_lines.append('end;')
        pascal_lines.append('')

    # Imprime Procedures
    for procedure in _java_class.procedure_declarations:
        procedure_arguments = _get_arguments(procedure)
        pascal_lines.append('procedure ' + procedure.procedure_name + '(' + procedure_arguments + ');')
        _append_local_declarations(procedure, pascal_lines)
        pascal_lines.append('begin')
        _append_assignments(indentation, procedure, pascal_lines)
        pascal_lines.append('end;')
        pascal_lines.append('')

    # Imprime o método Principal
    pascal_lines.append('begin')
    pascal_lines.append("   ")
    pascal_lines.append('end.')

    return pascal_lines
