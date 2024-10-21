import tkinter as tk

from interface.interface_peca import InterfacePeca

# EM CASO DE ALTERAÇÃO DO CÓDIGO, MODIFIQUE ESSA DOCUMENTAÇÃO SOBRE GRANDES MUDANÇAS.

# Descrição:
#       Cria a seção de peças do jogador no centro-inferior da tela. É responsavel 
#       por organizar os tiles de *apenas um* jogador em forma matricial.
#
# Interações:
#       Rack é construida pela Interface (__init__) no início do programa, e só é 
#       finalizada quando o jogo termina. 
#
# Notas:
#   --- É uma instancia de tk.Frame, e é gerenciado pelo pack do tkinter, não por grid.
#
#   --- Mesmo que ele sempre vá conter tiles, ele não deve ser o master de tile,
#       pois o mesmo deverá aparecer em cima de outros elementos da tela.

#   --- Rack atualmente instancia os  Tiles, mas isso deverá ser alterado 
#       eventualmente, quando tivermos um real gerenciador de tiles (Baralho).


class InterfaceSuporte:
    def __init__(
            self,
            master,
            canvas: tk.Canvas,
            linhas: int = 5,
            colunas: int = 10,
            tamanho_peca: int = 50,
            interface=None
        ):
        self.master = master
        self.interface = interface

        self.canvas = canvas
        self.tamanho_peca = tamanho_peca
        self.linhas = linhas
        self.colunas = colunas

        self.rect_bounds = [430, 700, 930, 930]
        self.offset = 0, +25

        self.tiles = []
        self.criar_rack()


    def criar_rack(self):
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))

        rack_width = self.tamanho_peca * self.colunas + 15
        rack_height = self.tamanho_peca * self.linhas + 15

        x_offset = (canvas_width - rack_width) // 2
        y_offset = canvas_height - rack_height - 20

        self.canvas.create_rectangle(
            x_offset,
            y_offset,
            x_offset + rack_width,
            y_offset + rack_height,
            outline="black",
            width=5
        )

    def criar_pecas(self):
        tiles = []
        i = 1

        for linha in range(self.linhas):
            for coluna in range(self.colunas):

                if i < 14:
                    tile = InterfacePeca(
                        master=self.canvas,
                        parent=self,
                        interface=self.interface,
                        numero=i,
                        tamanho=self.tamanho_peca,
                        linha=linha+14,
                        coluna=coluna+9,
                    )

                    tile.place(
                        x=self.rect_bounds[0]+20 + coluna*self.tamanho_peca,
                        y=self.rect_bounds[1]+25 + linha*self.tamanho_peca
                    )

                    i += 1
                    tiles.append(tile)

        self.tiles = tiles
