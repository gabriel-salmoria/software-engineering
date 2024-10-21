from logic.peca import Peca
from interface.interface_peca import InterfacePeca


class PecaCoringa(Peca):
    def __init__(
            self,
            tipo_coringa: str,
            cor: str,
        ):

        self.tipo_coringa = tipo_coringa
        self.numero = 99
        self.cor = cor

