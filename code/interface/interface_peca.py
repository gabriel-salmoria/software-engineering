import tkinter as tk


# Descrição:
#       Cria uma peça (tile) que pode ser exibida na interface do jogo. Cada 
#       tile mostra um número e possui uma cor de fundo.
#
# Interações:
#       A classe Tile é instanciada pela classe Rack ou pela classe Mesa 
#       (criar_matriz) durante o início do jogo. O ciclo de vida de um 
#       tile começa ao ser criado e termina quando o jogo é encerrado.
#
# Notas:
#   --- É uma instância de tk.Label e é gerenciada por pack do tkinter.
#
#   --- Cada tile é vinculado a eventoos de mouse, permitindo que o jogador 
#       o mova na interface através de cliques e arrastos.
#
#   --- Atualmente, a cor de fundo de cada tile é escolhida aleatoriamente 
#       de uma lista de cores, e a borda é escurecida para um melhor contraste.
#
#   --- Tile recebe Interface como master, pois tile deve ser capaz de alterar
#       posição entre Mesa e Rack, além de dever ser renderizada na frente de 
#       outros elementos, como a cor de fundo.


class InterfacePeca(tk.Label):
    def __init__(
            self,
            master,
            parent,
            interface,
            numero: int,
            cor: str,
            linha: int,
            coluna: int,
         ):

        super().__init__(
            master=master,
            text=numero,
            bg=cor,
            borderwidth=1,
            relief="solid",
            font=("Arial", 24),
            highlightbackground="black",
            highlightthickness=2
        )

        self.bind("<Button-1>", self.no_click)
        self.bind("<B1-Motion>", self.no_arrastar)
        self.bind("<ButtonRelease-1>", self.no_soltar)

        self.numero = numero
        self.cor = cor
        self.tamanho = 50
        self.linha = linha
        self.coluna = coluna

        self.parent = parent
        self.interface = interface

        self.start_x = 0
        self.start_y = 0

        self.place(
            x=coluna * self.tamanho,
            y=linha * self.tamanho+25,
            width=self.tamanho,
            height=self.tamanho
        )


    def no_click(self, evento: tk.Event) -> None:
        self.start_x = evento.x
        self.start_y = evento.y



    def no_arrastar(self, evento: tk.Event) -> None:
        x = self.winfo_x() - self.start_x + evento.x
        y = self.winfo_y() - self.start_y + evento.y

        self.place(x=x, y=y)
        self.lift()


    def no_soltar(self, evento: tk.Event) -> None:
        turno = self.interface.jogo.turnoAtual

        if self.verificar_colisao() or not turno:
            self.place(
                x=self.coluna * self.tamanho + self.parent.offset[0],
                y=self.linha * self.tamanho + self.parent.offset[1]
            )

            return

        self.efetuar_movimento()


    def efetuar_movimento(self):
        x, y = self.winfo_x(), self.winfo_y()
        mesa_bounds = self.interface.mesa_principal.rect_bounds
        suporte_bounds = self.interface.suporte_jogador.rect_bounds

        novo_local = None

        if (mesa_bounds[0] <= x <= mesa_bounds[2]) and (mesa_bounds[1] <= y <= mesa_bounds[3]):
            novo_local = self.interface.mesa_principal

        elif (suporte_bounds[0] <= x <= suporte_bounds[2]) and (suporte_bounds[1] <= y <= suporte_bounds[3]):
            novo_local = self.interface.suporte_jogador

        actor = self.interface.player_actor

        self.parent.pecas.remove(self)
        self.parent = novo_local
        self.parent.pecas.append(self)


        proxima_coluna = round((self.winfo_x() - 10) / self.tamanho)
        proxima_linha = round((self.winfo_y() - 10) / self.tamanho)

        novo_x = proxima_coluna * self.tamanho + 10
        novo_y = proxima_linha * self.tamanho + 10

        self.place(x=novo_x - 10, y=novo_y + 15)
        self.linha, self.coluna = proxima_linha, proxima_coluna

        if self.numero < 0:
            peca_info = f"{self.numero}_{self.cor}_{self.numero*-1}"
        else:
            peca_info = f"{self.numero}_{self.cor}"


        actor.jogo.listaJogadores[0].colocar_peca(
            peca_info,
            "mesa",
            str(proxima_coluna),
            str(proxima_linha)
        )

        actor.dogActor.send_move({
            "match_status" : actor.jogo.status_partida,
            "tipo" : "peca_movida",
            "peca" : peca_info,
            "local" : "mesa",
            "x" : str(proxima_coluna),
            "y" : str(proxima_linha)
            })



    def verificar_colisao(self) -> bool:
        x, y = self.winfo_x(), self.winfo_y()

        mesa_bounds = self.interface.mesa_principal.rect_bounds
        suporte_bounds = self.interface.suporte_jogador.rect_bounds

        novo_local = None

        if (mesa_bounds[0] <= x <= mesa_bounds[2]) and (mesa_bounds[1] <= y <= mesa_bounds[3]):
            novo_local = self.interface.mesa_principal

        elif (suporte_bounds[0] <= x <= suporte_bounds[2]) and (suporte_bounds[1] <= y <= suporte_bounds[3]):
            novo_local = self.interface.suporte_jogador

        if novo_local == None:
            return True

        tiles = novo_local.pecas

        proxima_coluna= round((self.winfo_x() - 10) / self.tamanho)
        proxima_linha = round((self.winfo_y() - 10) / self.tamanho)

        for tile in tiles:
            if tile.linha == proxima_linha and tile.coluna == proxima_coluna:
                return True

        return False


    # recebo o movimento do jogador externo e preciso atualizar
    # na interface para que a interfacePeca esteja correta
    def atualizar_posicao(self, local, x, y):
        self.parent.pecas.remove(self)

        if local == "mesa":
            self.parent = self.interface.mesa_principal
        elif local == "suporte":
            self.parent = self.interface.suporte_jogador

        self.parent.pecas.append(self)
        self.place(
                x = x*self.tamanho + self.parent.offset[0],
                y = y*self.tamanho + self.parent.offset[1]
            )
