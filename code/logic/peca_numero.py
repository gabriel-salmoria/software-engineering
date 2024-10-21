from logic.peca import Peca
from interface.interface_peca import InterfacePeca

class PecaNumero(Peca):
    def __init__(
            self,
            numero: int,
            cor: str,
        ):

        self.numero = numero
        self.cor = cor


    def get_cor(self):
        return self.cor


    def get_numero(self):
        return self.numero

