
class Jogador:
    def __init__(self, jogo):
        self.jogo = jogo
        self.pecas = self.get_pecas()

        self.vencedor = False
        self.turno = False

    def get_pecas(self) -> list:
        pecas = []

        for _ in range(14):
            peca = self.jogo.baralho.pegar_peca_aleatoria()
            pecas.append(peca)

        return pecas

    def checar_vitoria(self) -> bool:
        return len(self.pecas) == 0
