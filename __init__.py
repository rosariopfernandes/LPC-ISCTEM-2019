import syntax_analysis
import outputs
import subprocess
from flask import Flask, request
from flask import jsonify
from lexical_analysis import AuxiliarTables
from java_parser import JavaParser
from java_grammar import CONTEXT_FREE_GRAMMAR
from converters.pascal_converter import get_pascal_equivalent, JAVA_PASCAL_MAPPING

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def get():
    out = subprocess.check_output(['java', '-jar', '/home/rosariopfernandes/RosarioScript.jar', 'public class Hello { int x; }'])
    print(out)
    lines = request.json.split('\n')
    # TODO: Send this request.json to Java without splitting.
    # print('lines=', lines)

    if len(lines) == 0:
        exit()

    _lexical_analysis = AuxiliarTables()
    # TODO: Replace with Java lexical analysis
    response = _lexical_analysis.execute(lines)
    if response.get("code") == -1:
        return response
    else:
        # print(response.get("lexemes"))
        # print(response.get("symbols"))
        outputs.print_lexema_table(_lexical_analysis.get_lexeme_table())

        # outputs.print_symbol_table(_lexical_analysis.get_symbol_table())

        # [x] Declaração de variáveis do tipo primitivo local
        # [X] Declaração de variáveis do tipo primitivo global
        # [x] instruções de atribuições simples
        # [x] Funções sem retorno
        # [x] Funções com retorno
        # [ ] Estruturas de controlo (if e while)

        # Mantém-se. Executará depois das análises Java. Utilizará a tabela de lexemas do Java.
        parse_result = syntax_analysis.execute(_lexical_analysis.get_lexeme_table(), CONTEXT_FREE_GRAMMAR)

        if parse_result['code'] != -1:
            # TODO: Deal with the IndexError thrown here when the code cant be parsed by nltk
            java_tuple = JavaParser().get_class_declaration(parse_result['result'],
                                                            _lexical_analysis.get_lexeme_table().get_lexemes(),
                                                            JAVA_PASCAL_MAPPING)
            java_class = java_tuple[0]
            # print(response)
            if java_class is None:
                response = java_tuple[1]
                res = jsonify(response)
                res.headers.add('Access-Control-Allow-Origin', '*')
                return res
            else:
                response['java_class'] = java_tuple[1]
                pascal_lines = get_pascal_equivalent(java_class)
                response['result_lines'] = pascal_lines
                # print(response)
                res = jsonify(response)
                res.headers.add('Access-Control-Allow-Origin', '*')
                return res
                # for line in pascal_lines:
                #     print(line)
        else:
            res = jsonify(parse_result)
            res.headers.add('Access-Control-Allow-Origin', '*')
            return res


if __name__ == "__main__":
    app.run()
