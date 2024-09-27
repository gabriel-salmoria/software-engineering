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


class Rack(tk.Frame):
    def __init__(self, master: tk.Tk, linhas: int = 5, colunas: int = 10, tamanho_tile: int = 50):
        super().__init__(master)
        self.tamanho_tile = tamanho_tile
        self.linhas = linhas
        self.colunas = colunas
        self.criar_rack()

    def criar_rack(self) -> None:
        self.canvas = tk.Canvas(
            master=self,
            width=self.tamanho_tile * self.colunas + 20,
            height=self.tamanho_tile * self.linhas + 20,
            bg="lightgray"
        )

        self.canvas.pack(padx=10, pady=10)

        self.canvas.create_rectangle(
            5,
            5,
            self.tamanho_tile * self.colunas + 15,
            self.tamanho_tile * self.linhas + 15,
            outline="black",
            width=5
        )

        """" Parte desnecessária, colocada aqui só pra demonstração. """

        numero_tile = 1
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if numero_tile <= 14:
                    tile = Tile(
                        master=self.canvas,
                        numero=numero_tile,
                        tamanho=self.tamanho_tile,
                        linha=linha,
                        coluna=coluna
                    )
                    tile.place(
                        x=coluna * self.tamanho_tile + 10,
                        y=linha * self.tamanho_tile + 10
                    )
                    numero_tile += 1

