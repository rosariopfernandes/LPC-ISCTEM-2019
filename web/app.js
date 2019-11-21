require.config({ paths: { 'vs': 'package/min/vs' }});
let java_editor;
let pascal_editor;
let filename = 'Exemplo';
require(['vs/editor/editor.main'], function() {
    java_editor = monaco.editor.create(document.getElementById('source-container'), {
        value: [
            'public class HelloWorld {',
            '    public void main() {',
            '        int x;',
            '    }',
            '}'
        ].join('\n'),
        language: 'java',
        scrollBeyondLastLine: false,
    });

    // Comandos
    java_editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_S, function() {
        compileJavaCode();
    });

    java_editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_O, function() {
        document.getElementById('file-input').click();
    });

    document.getElementById('btn-novo').addEventListener('click', function (e) {
        document.getElementById('file-input').value = '';
        java_editor.setValue([
            'public class HelloWorld {',
            '    public void main() {',
            '        int x;',
            '    }',
            '}'
        ].join('\n'))
    });

    pascal_editor = monaco.editor.create(document.getElementById('destination-container'), {
        value: '{ O código Pascal aparecerá aqui }',
        language: 'pascal',
        scrollBeyondLastLine: false,
        readOnly: true,
        wordWrap: 'wordWrapColumn',
        wordWrapColumn: 45,
        wrappingIndent: "indent"
    });
});

function compileJavaCode() {
    fetch(new Request('http://localhost:5000'),{
        method: 'post',
        body: JSON.stringify(java_editor.getValue()),
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        }})
        .then(res => res.json())
        .then(function (response) {
            console.log(response);
            // Workaround para remover a linha de erro anterior
            java_editor.setValue(java_editor.getValue());
            if (response.code === -1) {
                document.getElementById('tables-container').style.visibility = 'hidden';
                pascal_editor.setValue('{ ' + response.message + ' }');
                // TODO: Adicionar uma caixa de erro
                if (response.line) {
                    decorations = [];
                    decorations[0] = { range: new monaco.Range(response.line,1,response.line,1), options: { isWholeLine: true, linesDecorationsClassName: 'myLineDecoration' }};
                    if (response.startCol && response.endCol) {
                        decorations[1] = { range: new monaco.Range(response.line,response.startCol+1,response.line,response.endCol+1), options: { inlineClassName: 'myInlineDecoration' }};
                    }
                    java_editor.deltaDecorations([], decorations);
                }
            } else {
                document.getElementById('tables-container').style.visibility = 'visible';
                filename = response.java_class.class_name;
                pascal_editor.setValue(response.result_lines.join('\n'));
                let table_lexemes = document.getElementById('table_lexemes');
                let table_symbols = document.getElementById('table_symbols');
                let lexemes = response.lexemes;
                let symbols = response.symbols;
                let content = "";
                table_lexemes.innerHTML = "";
                lexemes.forEach(function (lexeme) {
                    content += "<tr><td class='mdl-data-table__cell--non-numeric'>" + lexeme.token +
                        "</td><td class='mdl-data-table__cell--non-numeric'>"  + lexeme.classification + "</td><td>" +
                        lexeme.line + "</td></tr>";
                });
                table_lexemes.innerHTML = content;

                content = "";
                symbols.forEach(function (symbol) {
                    content += '<tr>' +
                        '<td class="mdl-data-table__cell--non-numeric">' + symbol.identifier + '</td>\n' +
                        '<td class="mdl-data-table__cell--non-numeric">' + symbol.category + '</td>\n' +
                        '<td class="mdl-data-table__cell--non-numeric">' + symbol.data_type + '</td>\n' +
                        '<td class="mdl-data-table__cell--non-numeric">' + symbol.memory_structure + '</td>\n' +
                        '<td>' + symbol.value + '</td>\n' +
                        '<td>' + symbol.params_nr + '</td>\n' +
                        '<td class="mdl-data-table__cell--non-numeric">' + symbol.params_sequence + '</td>\n' +
                        '<td class="mdl-data-table__cell--non-numeric">' + symbol.evaluation_strategy + '</td>\n' +
                        '<td class="mdl-data-table__cell--non-numeric">' + symbol.reference + '</td>\n' +
                        '<td>' + symbol.level + '</td>\n' +
                        '</tr>'
                });
                table_symbols.innerHTML = content;
            }
        })
        .catch(function (error) {
            document.getElementById('tables-container').style.visibility = 'hidden';
            console.log(error);
        });
}

function download_file() {
    let a = document.getElementById("save_file");
    let file = new Blob([pascal_editor.getValue()], {type: 'text/plain'});
    a.href = URL.createObjectURL(file);
    a.download = filename + '.pas';
}

let input = document.getElementById('file-input');

input.onchange = e => {
    let file = e.target.files[0];
    let reader = new FileReader();
    reader.readAsText(file,'UTF-8');

    // here we tell the reader what to do when it's done reading...
    reader.onload = readerEvent => {
        let content = readerEvent.target.result; // this is the content!
        java_editor.setValue(content);
    }
};
