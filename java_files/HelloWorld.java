public class HelloWorld {

    // declaração de variável global
    int varGlobal;
    boolean varGlobalA;

    // Função com retorno
    int funcaoComRetorno() {
        // declaração de variável local
        int a;
        varGlobalA = false;
        a = 13;
        return 20;
    }

    // Função sem retorno
    public void main() {
        varGlobal = 10;
        // estrutura if
        if ( varGlobal > 15) {
            varGlobalA = true;
        } else {
            varGlobalA = false;
        }

        // estrutura while
        while (varGlobal < 20) {
            varGlobalA = true;
        }
    }
}