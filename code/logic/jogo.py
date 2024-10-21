from interface.interface import Interface

from logic.baralho import Baralho
from logic.mesa import Mesa
from logic.jogador import Jogador

class Jogo:
    def __init__(self):
        self.Mesa = Mesa(
            linhas=10,
            colunas=25,
        )

        self.baralho = Baralho()
        self.jogador = Jogador(self)

        self.interface = Interface(self, self.jogador)
        self.interface.mainloop()
