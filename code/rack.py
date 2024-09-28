import tkinter as tk

from tile import Tile

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


class Rack:
    def __init__(self, master, canvas: tk.Canvas, linhas: int = 5, colunas: int = 10, tamanho_tile: int = 50, interface=None):
        self.canvas = canvas
        self.tamanho_tile = tamanho_tile
        self.linhas = linhas
        self.colunas = colunas
        self.master = master
        self.interface = interface
        self.rect_bounds = [310, 610, 760, 810]
        self.offset = 0, +25
        self.criar_rack()


    def criar_rack(self):
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))

        # Calculate the width and height of the rack
        rack_width = self.tamanho_tile * self.colunas + 15
        rack_height = self.tamanho_tile * self.linhas + 15

        # Calculate x offset to center the rack horizontally
        x_offset = (canvas_width - rack_width) // 2

        # Set the y position to be at the bottom of the canvas
        y_offset = canvas_height - rack_height - 20  # Add a margin from the bottom

        # Create the rack rectangle at the centered bottom position
        self.canvas.create_rectangle(
            x_offset,
            y_offset,
            x_offset + rack_width,
            y_offset + rack_height,
            outline="black",
            width=5
        )

    def criar_tiles(self):
        numero_tile = 1
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if numero_tile <= 14:
                    tile = Tile(
                        master=self.canvas,
                        numero=numero_tile,
                        tamanho=self.tamanho_tile,
                        linha=linha+12,
                        coluna=coluna+6,
                        parent=self,
                        interface=self.interface
                    )
                    tile.place(
                        x=290 + coluna * self.tamanho_tile + 10,
                        y=615 + linha * self.tamanho_tile + 10  # Adjust Y based on Rack's offset
                    )
                    numero_tile += 1

        
