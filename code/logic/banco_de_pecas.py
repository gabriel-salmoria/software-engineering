from random import choice

class BancoDePecas:
    def __init__(self, jogo):
        self.pecas = []
        self.jogo = jogo

    def pegar_peca(self): # -> Peca
        peca = choice(self.pecas)
        self.pecas.remove(peca)
        return peca

    def efetuar_distribuicao_pecas(self):
        mao_jogador1 = []
        mao_jogador2 = []

        for _ in range(14):
            mao_jogador1.append(self.pegar_peca())
        self.jogo.listaJogadores[0].receber_pecas(mao_jogador1)

        for _ in range(14):
            mao_jogador2.append(self.pegar_peca())
        self.jogo.listaJogadores[1].receber_pecas(mao_jogador2)
