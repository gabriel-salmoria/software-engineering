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
#   --- Cada tile é vinculado a eventos de mouse, permitindo que o jogador 
#       o mova na interface através de cliques e arrastos.
#
#   --- Atualmente, a cor de fundo de cada tile é escolhida aleatoriamente 
#       de uma lista de cores, e a borda é escurecida para um melhor contraste.
#
#   --- Tile recebe Interface como master, pois tile deve ser capaz de alterar
#       posição entre Mesa e Rack, além de dever ser renderizada na frente de 
#       outros elementos, como a cor de fundo.


class Tile(tk.Label):
    def __init__(self, master, numero: int, tamanho: int, linha: int, coluna: int, parent, interface):
        super().__init__(
            master=master,
            text=numero,
            bg=random.choice(["lightblue", "lightgreen", "lightcoral", "lightyellow"]),
            borderwidth=1,
            relief="solid",
            font=("Arial", 24),
            highlightbackground="black",
            highlightthickness=2
        )

        self.bind("<Button-1>", self.no_click)
        self.bind("<B1-Motion>", self.no_arrastar)
        self.bind("<ButtonRelease-1>", self.no_liberar)

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

    def no_liberar(self, evento: tk.Event) -> None:
        x, y = self.winfo_x(), self.winfo_y()

        new_parent = self.detectar_novo_parent(x, y)

        if new_parent is None or self.verifica_colisao(new_parent):
            self.place(
                x=self.coluna * self.tamanho + self.parent.offset[0],
                y=self.linha * self.tamanho + self.parent.offset[1]
            )
        else:

            self.parent.tiles.remove(self)
            self.parent = new_parent
            self.parent.tiles.append(self)

            coluna_mais_proxima = round((self.winfo_x() - 10) / self.tamanho)
            linha_mais_proxima = round((self.winfo_y() - 10) / self.tamanho)

            novo_x = coluna_mais_proxima * self.tamanho + 10
            novo_y = linha_mais_proxima * self.tamanho + 10

            self.place(x=novo_x - 10, y=novo_y + 15)
            self.linha, self.coluna = linha_mais_proxima, coluna_mais_proxima

    def verifica_colisao(self, novo_parent):
        """ Verifica se o tile está sendo largado em cima de outro tile. """
        tiles = novo_parent.tiles

        coluna_mais_proxima = round((self.winfo_x() - 10) / self.tamanho)
        linha_mais_proxima = round((self.winfo_y() - 10) / self.tamanho)

        for tile in tiles:
            if tile != self:
                if tile.linha == linha_mais_proxima and tile.coluna == coluna_mais_proxima:
                    return True

        return False  # Sem colisão

    def detectar_novo_parent(self, x, y):
        mesa_bounds = self.interface.mesa_principal.rect_bounds
        rack_bounds = self.interface.rack.rect_bounds

        if (mesa_bounds[0] <= x <= mesa_bounds[2]) and (mesa_bounds[1] <= y <= mesa_bounds[3]):
            return self.interface.mesa_principal

        elif (rack_bounds[0] <= x <= rack_bounds[2]) and (rack_bounds[1] <= y <= rack_bounds[3]):
            return self.interface.rack

        return None
