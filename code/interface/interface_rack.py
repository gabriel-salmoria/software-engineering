import tkinter as tk

from interface.interface_piece import InterfacePiece

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


class InterfaceRack:
    def __init__(
            self,
            master,
            canvas: tk.Canvas,
            rows: int = 5,
            columns: int = 10,
            piece_size: int = 50,
            interface=None
        ):
        self.master = master
        self.interface = interface

        self.canvas = canvas
        self.piece_size = piece_size
        self.rows = rows
        self.columns = columns

        self.rect_bounds = [430, 700, 930, 930]
        self.offset = 0, +25

        self.tiles = []
        self.create_rack()


    def create_rack(self):
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))

        rack_width = self.piece_size * self.columns + 15
        rack_height = self.piece_size * self.rows + 15

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

    def create_pieces(self):
        tiles = []
        piece_number = 1

        for row in range(self.rows):
            for column in range(self.columns):

                if piece_number <= 14:

                    tile = InterfacePiece(
                        master=self.canvas,
                        parent=self,
                        interface=self.interface,
                        number=piece_number,
                        size=self.piece_size,
                        row=row+14,
                        column=column+9,
                    )

                    tile.place(
                        x=440 + column*self.piece_size + 10,
                        y=715 + row*self.piece_size + 10
                    )

                    piece_number += 1
                    tiles.append(tile)

        self.tiles = tiles
