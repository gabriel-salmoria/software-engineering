import random
from logic.peca_numero import PecaNumero
from logic.peca_coringa import PecaCoringa



class Baralho:
    def __init__(self):
        self.pecas = self.inicializar_pecas()


    def inicializar_pecas(self) -> list:
        pecas = []
        cores = ["lightblue", "lightgreen", "lightcoral", "lightyellow"]

        for numero in range(1,13):
            for cor in cores:
                peca = PecaNumero(numero=numero, cor=cor)
                pecas.append(peca)

        for cor in cores:
            peca = PecaCoringa(tipo_coringa='normal', cor=cor)
            pecas.append(peca) 

        return pecas


    def pegar_peca_aleatoria(self):
        peca = random.choice(self.pecas)
        self.pecas.remove(peca)

        return peca





