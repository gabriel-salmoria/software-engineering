from logic.peca import Peca

class PecaCoringa(Peca):
    def __init__(self, valor, cor, tipoCoringa):
        self.valor = valor
        self.cor = cor
        self.tipoCoringa = tipoCoringa
        self.int = None
