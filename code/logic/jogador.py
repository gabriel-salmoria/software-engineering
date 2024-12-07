

class Jogador:
    def __init__(self, jogo):
        self.cor = None
        self.seu_turno = False
        self.vencedor = False
        self.nome = ""
        self.pecasMao = []
        self.jogo = jogo


    def atualizar_turno(self):
        self.seu_turno = not self.seu_turno


    def passar_vez(self):
        seu_turno = self.jogo.verificar_turno()

        if seu_turno:
            jogada_valida = self.jogo.validar_jogada()

            if jogada_valida:
                vencedor = self.get_vencedor()

                if vencedor:
                    self.jogo.finalizar_partida()

                else:
                    self.jogo.efetuar_passagem_vez()

            else:
                self.comprar_peca()
                self.jogo.efetuar_passagem_vez()

        else:
            print("nao eh seu turno") # TODO: change

        self.jogo.interface_jogador.send_move()
        self.jogo.interface.atualizar_elementos()



    def efetuar_passagem_vez(self):
        self.jogo.efetuar_passagem_vez()



    def colocar_peca(self, peca: "Peca", x: int, y: int):
        pass
        

    def receber_pecas(self, pecas: list):
        self.pecasMao = pecas


    def comprar_peca(self):
        peca = self.jogo.banco_de_pecas.pegar_peca()
        self.pecasMao.append(peca)


    def inicializar(self, nome: str, cor: int):
        self.nome = nome
        self.cor = cor


    def verificar_turno(self) -> bool:
        return self.seu_turno


    def get_vencedor(self) -> bool:
        return len(self.pecasMao) == 0
