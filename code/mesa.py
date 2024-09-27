import tkinter as tk

# Descrição:
#       A classe Mesa representa a área de jogo onde os tiles de *todos* os 
#       players são exibidos. Ela organiza os tiles em uma matriz.
#
# Interações:
#       A Mesa é criada logo no início do jogo e serve como o cenário 
#       principal para os tiles. Ela permanece ativa até que o jogo termine, 
#       proporcionando um ambiente contínuo para o jogador.
#
# Notas:
#   --- A Mesa é um tipo de tk.Frame, utilizando o método pack do tkinter.
#
#   --- Ela contém um canvas onde os tiles são desenhados, com dimensões 
#       determinadas pelo número de linhas e colunas, assim como pelo 
#       tamanho de cada tile.


class Mesa(tk.Frame):
    def __init__(self, master: tk.Tk, linhas: int = 10, colunas: int = 20, tamanho_tile: int = 50):
        super().__init__(master)
        self.tamanho_tile = tamanho_tile
        self.linhas = linhas
        self.colunas = colunas
        self.criar_matriz()

    def criar_matriz(self) -> None:
        self.canvas = tk.Canvas(
            master=self,
            width=self.tamanho_tile * self.colunas + 20,
            height=self.tamanho_tile * self.linhas + 20,
            bg="white"
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

