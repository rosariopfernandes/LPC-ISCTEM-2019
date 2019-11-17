from models.class_declaration import ClassDeclaration
from models.variable_assignment import VariableAssignment
from models.method_call import MethodCall

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


def _append_assignments(method, lines):
    for assignment in method.assignments:
        if type(assignment) == VariableAssignment:
            # Declaração de variáveis
            lines.append('   ' + assignment.variable_name + ' := ' + assignment.value + ';')
        else:
            # Chamada de métodos
            lines.append('   ' + assignment.method_name + '(' + _get_passed_arguments(assignment) + ');')
            # TODO: add structures if and while here


def get_pascal_equivalent(_java_class: ClassDeclaration):

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
        _append_assignments(_function, pascal_lines)
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
        _append_assignments(procedure, pascal_lines)
        pascal_lines.append('end;')
        pascal_lines.append('')

    # Imprime o método Principal
    pascal_lines.append('begin')
    pascal_lines.append("   ")
    pascal_lines.append('end.')

    return pascal_lines
