from nltk import CFG

# Palavras Reservadas
RESERVED_WORDS = ['public', 'class', 'for', 'while', 'if', 'static', 'private', 'return', 'else']

# Tipos primitivos
PRIMITIVE_TYPES = ['int', 'char', 'double', 'float', 'void', 'boolean', 'short', 'long', 'byte']

# Símbolos Especiais
# TODO: classificar multiplicacao(*) e divisão (/). Tem conflito com comentários
SYMBOLS = ['+', '-', '=', '{', '}', '[', ']', '<', '>']

CONTEXT_FREE_GRAMMAR = CFG.fromstring(
    """
    declaracao_classe -> modificador "class" identificador inicio_bloco corpo_classe fim_bloco

    corpo_classe -> declaracao_variavel
    corpo_classe -> declaracao_metodo
    corpo_classe -> declaracao_variavel corpo_classe
    corpo_classe -> declaracao_metodo corpo_classe

    declaracao_metodo -> tipo_dado_sem_retorno identificador '(' lista_parametros ')' inicio_bloco corpo_metodo fim_bloco
    declaracao_metodo -> tipo_dado_com_retorno identificador '(' lista_parametros ')' inicio_bloco corpo_metodo "return" retorno simbolo_fim_instrucao fim_bloco
    declaracao_metodo -> modificador tipo_dado_sem_retorno identificador '(' lista_parametros ')' inicio_bloco corpo_metodo fim_bloco
    declaracao_metodo -> modificador tipo_dado_com_retorno identificador '(' lista_parametros ')' inicio_bloco corpo_metodo "return" retorno simbolo_fim_instrucao fim_bloco
    retorno -> identificador | valor
    
    lista_parametros ->
    lista_parametros -> tipo_dado_com_retorno identificador
    lista_parametros -> tipo_dado_com_retorno identificador simbolo_separador lista_parametros

    corpo_metodo -> 
    corpo_metodo -> atribuicao_variavel
    corpo_metodo -> declaracao_variavel
    corpo_metodo -> chamada_metodo
    corpo_metodo -> estrutura_if
    corpo_metodo -> estrutura_while
    corpo_metodo -> atribuicao_variavel corpo_metodo 
    corpo_metodo -> declaracao_variavel corpo_metodo
    corpo_metodo -> chamada_metodo corpo_metodo
    corpo_metodo -> estrutura_if corpo_metodo
    corpo_metodo -> estrutura_while corpo_metodo
    
    estrutura_if -> "if" '(' condicao ')' inicio_bloco corpo_metodo fim_bloco estrutura_else
    estrutura_if -> "if" '(' condicao ')' inicio_bloco corpo_metodo fim_bloco
    estrutura_else -> "else" inicio_bloco corpo_metodo fim_bloco
    estrutura_while -> "while" '(' condicao ')' inicio_bloco corpo_metodo fim_bloco
    condicao -> identificador
    condicao -> constante_booleana
    condicao -> operando operador_comparacao operando
    
    operador_comparacao -> '>' | '<' | '>' '=' | '<' '=' | '=' '='
    operando -> identificador | constante_inteira | constante_real

    declaracao_variavel -> tipo_dado_com_retorno identificador simbolo_fim_instrucao | modificador tipo_dado_com_retorno identificador simbolo_fim_instrucao
    declaracao_variavel -> tipo_dado_com_retorno identificador simbolo_atribuicao valor simbolo_fim_instrucao | modificador tipo_dado_com_retorno identificador simbolo_atribuicao valor simbolo_fim_instrucao
    
    modificador -> "public" | "private" | "protected"

    atribuicao_variavel -> identificador simbolo_atribuicao valor simbolo_fim_instrucao
    atribuicao_variavel -> identificador simbolo_atribuicao chamada_metodo simbolo_fim_instrucao

    tipo_dado_com_retorno -> "int" | "char" | "byte" | "long" | "short" | "boolean" | "float" | "double"
    tipo_dado_sem_retorno -> "void"

    chamada_metodo -> identificador '(' lista_argumentos ')' simbolo_fim_instrucao
    
    lista_argumentos ->
    lista_argumentos -> identificador
    lista_argumentos -> identificador simbolo_separador lista_argumentos

    inicio_bloco -> '{'
    simbolo_separador -> ','
    simbolo_atribuicao -> '='
    simbolo_fim_instrucao -> ';'
    fim_bloco -> '}'

    identificador -> inicio_identificador
    identificador -> inicio_identificador corpo_identificador
    inicio_identificador -> letra
    corpo_identificador -> letra | constante_inteira
    corpo_identificador -> letra corpo_identificador | constante_inteira corpo_identificador

    palavra -> letra
    palavra -> letra palavra
    letra -> 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
    letra -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '_'

    valor -> constante_inteira | constante_booleana | constante_real | constante_caracter

    constante_inteira -> digito
    constante_inteira -> digito constante_inteira
    digito -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    
    constante_booleana -> "true" | "false"
    
    constante_real -> constante_inteira separador constante_inteira
    constante_real -> constante_inteira separador constante_inteira 'f'
    separador -> '.'
    
    constante_caracter -> "'" caracter "'"
    caracter -> letra | digito | '*' | '|' | '/' | '!' | '#' | '$' | '%' | '&'
    """
)
