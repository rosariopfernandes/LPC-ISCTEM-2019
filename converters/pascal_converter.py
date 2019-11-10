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
        variable_output = '   ' + variavel.variable_name + ': ' + variavel.data_type
        if variavel.value is not None:
            variable_output += ' := ' + variavel.value
        print(variable_output + ';')
    print()

    # Imprime Functions TODO

    # Imprime Procedures
    for procedure in _java_class.procedure_declarations:
        print('procedure ' + procedure.procedure_name + '();')
        print('begin')
        for assignment in procedure.assignments:
            print('   ' + assignment.variable_name + ' := ' + assignment.value + ';')
        print('end;')
        print()

    # Imprime o método Principal
    print('begin')
    print("   writeln('Hello World')")
    print('end.')
