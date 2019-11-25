import syntax_analysis
import outputs
import subprocess
import json
from flask import Flask, request
from flask import jsonify
from lexeme_table import Lexema
from semantic_analysis import SemanticAnalysis
from java_grammar import CONTEXT_FREE_GRAMMAR
from converters.pascal_converter import get_pascal_equivalent, JAVA_PASCAL_MAPPING

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def get():
    out = subprocess.check_output(['java', '-jar', 'AnalisadorJava.jar', request.json])
    response = json.loads(out)

    if response.get("code") == -1:
        return response
    else:
        lexemes_list = []
        for lexeme in response['lexemes']:
            lexemes_list.append(Lexema(lexeme['token'], lexeme['classification'], lexeme['line']))
        outputs.print_lexema_table(lexemes_list)

        parse_result = syntax_analysis.execute(lexemes_list, CONTEXT_FREE_GRAMMAR)
        if parse_result['code'] != -1:
            try:
                java_tuple = SemanticAnalysis().get_class_declaration(parse_result['result'], lexemes_list,
                                                                      JAVA_PASCAL_MAPPING)
                java_class = java_tuple[0]
                if java_class is None:
                    response = java_tuple[1]
                    res = jsonify(response)
                    res.headers.add('Access-Control-Allow-Origin', '*')
                    return res
                else:
                    response['java_class'] = java_tuple[1]
                    pascal_lines = get_pascal_equivalent(java_class)
                    response['result_lines'] = pascal_lines
                    response['symbols'] = java_tuple[2]
                    response['code'] = 200
                    res = jsonify(response)
                    res.headers.add('Access-Control-Allow-Origin', '*')
                    return res
            except IndexError:
                return {
                    "code": -1,
                    "message": "Erro Sintático. Número de linha não disponível."
                }
        else:
            res = jsonify(parse_result)
            res.headers.add('Access-Control-Allow-Origin', '*')
            return res


if __name__ == "__main__":
    app.run()
