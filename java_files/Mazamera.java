public class Mazamera {
    private boolean sofreu;
    private int vezes_que_sofreu;

    public void main() {
        sofreu = true;
        vezes_que_sofreu = 3;
        guiguigui();
    }

    private void dizerGui() {
        // Imprimir "gui"
    }

    private void guiguigui() {
        int i;
        boolean estaoAFugir;
        i = 0;
        while (i < vezes_que_sofreu) {
            dizerGui();
        }
        if (i == 3) {
            estaoAFugir = true;
        }
    }
}