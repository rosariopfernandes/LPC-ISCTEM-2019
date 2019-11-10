import file_operations
import lexical_analysis
import outputs
from auxiliar_tables import AuxiliarTables
from java_parser import JavaParser
from java_grammar import CONTEXT_FREE_GRAMMAR
from converters.pascal_converter import print_pascal_equivalent, JAVA_PASCAL_MAPPING

lines = file_operations.read_lines_from_file('java_files/Ex.java')

if len(lines) == 0:
    exit()

tables = AuxiliarTables()
tables.fill_tables(lines)

outputs.print_lexema_table(tables.get_lexeme_table())

outputs.print_symbol_table(tables.get_symbol_table())

# [x] Declaração de variáveis do tipo primitivo local
# [X] Declaração de variáveis do tipo primitivo global
# [x] instruções de atribuições simples
# [x] Funções sem retorno
# [x] Funções com retorno
# [ ] Estruturas de controlo (if e while)

parse_result = lexical_analysis.execute(tables.get_lexeme_table(), CONTEXT_FREE_GRAMMAR)

if parse_result:
    java_class = JavaParser().get_class_declaration(parse_result, tables.get_symbol_table().get_identifiers(),
                                                    JAVA_PASCAL_MAPPING)
    print_pascal_equivalent(java_class)
