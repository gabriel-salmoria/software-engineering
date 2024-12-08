from interface.interface_peca import InterfacePeca

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
        self.jogo.efetuar_passagem_vez()
        return

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


    def colocar_peca(self, peca, local, x: int, y: int):
        valor, cor = peca.split("-")
        pecas_dispostas= self.jogo.mesa.pecas_dispostas
        x, y = int(x), int(y)
        if local == "mesa":
            for i in range(len(pecas_dispostas)):
                for j in range(len(pecas_dispostas[0])):
                    peca = pecas_dispostas[i][j]

                    if peca != None and str(peca.valor) == valor and str(peca.cor) == cor:
                        self.jogo.mesa.pecas_dispostas[i][j] = None
                        self.jogo.mesa.pecas_dispostas[x][y] = peca
                        peca.int.atualizar_posicao(local, x, y)
                        return

            for peca in self.pecasMao:
                if str(peca.valor) == valor and str(peca.cor) == cor:
                    if type(peca.int) != InterfacePeca:
                        interface = self.jogo.interface_jogador.interface
                        mesa = interface.mesa_principal
                        peca.int = InterfacePeca(
                                master=mesa.canvas,
                                parent=mesa,
                                interface=interface,
                                cor = peca.cor,
                                numero=peca.valor,
                                linha=y,
                                coluna=x,
                                )

                        mesa.pecas.append(peca.int)

                    peca.int.atualizar_posicao(local, x, y)
                    self.jogo.mesa.pecas_dispostas[x][y] = peca
                    self.pecasMao.remove(peca)

                    return


    def receber_pecas(self, pecas: list):
        self.pecasMao = pecas


    def comprar_peca(self):
        peca = self.jogo.bancoDePecas.comprar_peca()
        self.pecasMao.append(peca)


    def inicializar(self, nome: str, cor: int):
        self.nome = nome
        self.cor = cor


    def verificar_turno(self) -> bool:
        return self.seu_turno


    def get_vencedor(self) -> bool:
        return len(self.pecasMao) == 0
