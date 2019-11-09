import file_operations
import lexical_analysis
import outputs
from auxiliar_tables import AuxiliarTables
from pascal_converter import PascalConverter
from java_grammar import CONTEXT_FREE_GRAMMAR

lines = file_operations.read_lines_from_file('Ex.java')

if len(lines) == 0:
    exit()

tables = AuxiliarTables()
tables.fill_tables(lines)

outputs.print_lexema_table(tables.get_lexeme_table())

outputs.print_symbol_table(tables.get_symbol_table())

# [ ] Declaração de variáveis do tipo primitivo local
# [X] Declaração de variáveis do tipo primitivo global TODO: char, boolean, real
# [ ] instruções de atribuições simples
# [ ] Funções sem retorno
# [ ] Funções com retorno
# [ ] Estruturas de controlo (if e while)

parse_result = lexical_analysis.execute(tables.get_lexeme_table(), CONTEXT_FREE_GRAMMAR)

if parse_result:
    PascalConverter().print_corresponding_code(parse_result, tables.get_symbol_table().get_identifiers())
