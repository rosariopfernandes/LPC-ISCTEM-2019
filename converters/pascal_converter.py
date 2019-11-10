from models.class_declaration import ClassDeclaration


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


def print_pascal_equivalent(_java_class: ClassDeclaration):
    # Imprime nome do programa
    print('program ' + _java_class.class_name + ';')
    print()

    # Imprime variáveis globais
    print('var')
    for variavel in _java_class.variable_declarations:
        declaration_output = '   ' + variavel.variable_name + ': ' + variavel.data_type
        if variavel.value is not None:
            declaration_output += ' := ' + variavel.value
        print(declaration_output + ';')
    print()

    # Imprime Functions
    for _function in _java_class.function_declarations:
        procedure_arguments = ''
        for argument in _function.arguments:
            procedure_arguments += argument.variable_name + ': ' + argument.data_type + ', '
        if len(procedure_arguments) > 0:
            procedure_arguments = procedure_arguments[:-2]
        print('function ' + _function.function_name + '(' + procedure_arguments + '): ' + _function.data_type + ';')
        for declaration in _function.local_declarations:
            declaration_output = '   ' + declaration.variable_name + ': ' + declaration.data_type
            if declaration.value is not None:
                declaration_output += ' := ' + declaration.value
            print(declaration_output + ';')
        print('begin')
        for assignment in _function.assignments:
            print('   ' + assignment.variable_name + ' := ' + assignment.value + ';')
        print('end;')
        print()

    # Imprime Procedures
    for procedure in _java_class.procedure_declarations:
        procedure_arguments = ''
        for argument in procedure.arguments:
            procedure_arguments += argument.variable_name + ': ' + argument.data_type + ', '
        if len(procedure_arguments) > 0:
            procedure_arguments = procedure_arguments[:-2]
        print('procedure ' + procedure.procedure_name + '(' + procedure_arguments + ');')
        print('var')
        for declaration in procedure.local_declarations:
            declaration_output = '   ' + declaration.variable_name + ': ' + declaration.data_type
            if declaration.value is not None:
                declaration_output += ' := ' + declaration.value
            print(declaration_output + ';')
        print('begin')
        for assignment in procedure.assignments:
            print('   ' + assignment.variable_name + ' := ' + assignment.value + ';')
        print('end;')
        print()

    # Imprime o método Principal
    print('begin')
    print("   writeln('Hello World')")
    print('end.')
