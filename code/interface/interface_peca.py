import tkinter as tk
import random


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
            tamanho: int,
            linha: int,
            coluna: int,
         ):

        super().__init__(
            master=master,
            text=numero,
            bg=random.choice(['lightblue', 'lightcoral', 'lightyellow', 'lightgreen']),
            borderwidth=1,
            relief="solid",
            font=("Arial", 24),
            highlightbackground="black",
            highlightthickness=2
        )

        self.bind("<Button-1>", self.no_click)
        self.bind("<B1-Motion>", self.no_arrastar)
        self.bind("<ButtonRelease-1>", self.no_soltar)

        self.tamanho = tamanho
        self.linha = linha
        self.coluna = coluna

        self.parent = parent
        self.interface = interface

        self.start_x = 0
        self.start_y = 0

        self.place(
            x=coluna * tamanho + 10,
            y=linha * tamanho + 10,
            width=tamanho,
            height=tamanho
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
        x, y = self.winfo_x(), self.winfo_y()

        novo_local = self.detectar_caixa(x, y)

        if novo_local is None or self.verificar_colisao(novo_local):
            self.place(
                x=self.coluna * self.tamanho + self.parent.offset[0],
                y=self.linha * self.tamanho + self.parent.offset[1]
            )

            return

        self.parent.tiles.remove(self)
        self.parent = novo_local
        self.parent.tiles.append(self)

        proxima_coluna = round((self.winfo_x() - 10) / self.tamanho)
        proxima_linha = round((self.winfo_y() - 10) / self.tamanho)

        novo_x = proxima_coluna * self.tamanho + 10
        novo_y = proxima_linha * self.tamanho + 10

        self.place(x=novo_x - 10, y=novo_y + 15)
        self.linha, self.coluna = proxima_linha, proxima_coluna



    def verificar_colisao(self, novo_local) -> bool:
        """ Verify if the current tile has been placed into another tile. """

        tiles = novo_local.tiles

        proxima_coluna= round((self.winfo_x() - 10) / self.tamanho)
        proxima_linha = round((self.winfo_y() - 10) / self.tamanho)

        for tile in tiles:
            if tile != self:
                if tile.linha == proxima_linha and tile.coluna == proxima_coluna:
                    return True

        return False


    def detectar_caixa(self, x: int, y: int):
        """ Detect if the tile has been placed inside a correct area. """

        mesa_bounds = self.interface.mesa_principal.rect_bounds
        suporte_bounds = self.interface.suporte_jogador.rect_bounds

        if (mesa_bounds[0] <= x <= mesa_bounds[2]) and (mesa_bounds[1] <= y <= mesa_bounds[3]):
            return self.interface.mesa_principal

        elif (suporte_bounds[0] <= x <= suporte_bounds[2]) and (suporte_bounds[1] <= y <= suporte_bounds[3]):
            return self.interface.suporte_jogador

        return None
