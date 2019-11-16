import file_operations
import syntax_analysis
import outputs
from lexical_analysis import AuxiliarTables
from java_parser import JavaParser
from java_grammar import CONTEXT_FREE_GRAMMAR
from converters.pascal_converter import print_pascal_equivalent, JAVA_PASCAL_MAPPING

lines = file_operations.read_lines_from_file('java_files/Ex.java')

if len(lines) == 0:
    exit()

_lexical_analysis = AuxiliarTables()
response = _lexical_analysis.execute(lines)
if response.get("code") == -1:
    print(response.get("message"))
else:
    # print(response.get("lexemes"))
    # print(response.get("symbols"))
    outputs.print_lexema_table(_lexical_analysis.get_lexeme_table())

    outputs.print_symbol_table(_lexical_analysis.get_symbol_table())

    # [x] Declaração de variáveis do tipo primitivo local
    # [X] Declaração de variáveis do tipo primitivo global
    # [x] instruções de atribuições simples
    # [x] Funções sem retorno
    # [x] Funções com retorno
    # [ ] Estruturas de controlo (if e while)

    parse_result = syntax_analysis.execute(_lexical_analysis.get_lexeme_table(), CONTEXT_FREE_GRAMMAR)

    if parse_result:
        java_tuple = JavaParser().get_class_declaration(parse_result,
                                                        _lexical_analysis.get_symbol_table().get_identifiers(),
                                                        JAVA_PASCAL_MAPPING)
        java_class = java_tuple[0]
        response = java_tuple[1]
        # print(response)
        if java_class is not None:
            print_pascal_equivalent(java_class)
