class Identificador(object):
    id: str
    categoria: str
    tipo: str
    estrutura_memoria: str
    valor: str
    nr_params: int
    seq_params: str
    forma_passagem: str
    ref: str
    nivel: str

    def __init__(self, id, categoria, tipo, estrutura_memoria, valor, nr_params,
                 seq_params, forma_passagem, ref, nivel):
        self.id = id
        self.categoria = categoria
        self.tipo = tipo
        self.estrutura_memoria = estrutura_memoria
        self.valor = valor
        self.nr_params = nr_params
        self.seq_params = seq_params
        self.forma_passagem = forma_passagem
        self.ref = ref
        self.nivel = nivel

