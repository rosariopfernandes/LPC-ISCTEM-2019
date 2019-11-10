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


def _print_local_declarations(method):
    if len(method.local_declarations) > 0:
        print('var')
    for declaration in method.local_declarations:
        declaration_output = '   ' + declaration.variable_name + ': ' + declaration.data_type
        if declaration.value is not None:
            declaration_output += ' := ' + declaration.value
        print(declaration_output + ';')


def _print_assignemnts(method):
    for assignment in method.assignments:
        if type(assignment) == VariableAssignment:
            # Declaração de variáveis
            print('   ' + assignment.variable_name + ' := ' + assignment.value + ';')
        else:
            # Chamada de métodos
            print('   ' + assignment.method_name + '(' + _get_passed_arguments(assignment) + ');')
            # TODO: add structures if and while here


def print_pascal_equivalent(_java_class: ClassDeclaration):
    # Imprime nome do programa
    print('program ' + _java_class.class_name + ';')
    print()

    # Imprime variáveis globais
    if len(_java_class.variable_declarations) > 0:
        print('var')
    for variavel in _java_class.variable_declarations:
        declaration_output = '   ' + variavel.variable_name + ': ' + variavel.data_type
        if variavel.value is not None:
            declaration_output += ' := ' + variavel.value
        print(declaration_output + ';')
    print()

    # Imprime Functions
    for _function in _java_class.function_declarations:
        function_arguments = _get_arguments(_function)
        print('function ' + _function.function_name + '(' + function_arguments + '): ' + _function.data_type + ';')
        _print_local_declarations(_function)
        print('begin')
        _print_assignemnts(_function)
        # Imprimir o retorno:
        print('   ' + _function.function_name + ' := ' + _function.return_value + ';')
        print('end;')
        print()

    # Imprime Procedures
    for procedure in _java_class.procedure_declarations:
        procedure_arguments = _get_arguments(procedure)
        print('procedure ' + procedure.procedure_name + '(' + procedure_arguments + ');')
        _print_local_declarations(procedure)
        print('begin')
        _print_assignemnts(procedure)
        print('end;')
        print()

    # Imprime o método Principal
    print('begin')
    print("   writeln('Hello World');")
    print('end.')
