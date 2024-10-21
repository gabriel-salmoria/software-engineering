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


class InterfaceMesa:
    def __init__(
            self,
            master,
            canvas: tk.Canvas,
            linhas: int = 10,
            colunas: int = 20,
            tamanho_peca: int = 50
        ):
        self.master = master

        self.canvas = canvas
        self.tamanho_peca = tamanho_peca

        self.linhas = linhas
        self.colunas = colunas
        self.tiles = []

        self.rect_bounds = [90, 50, 1280, 480]
        self.offset = 0, 25

        self.criar_matriz()

    def criar_matriz(self):
        canvas_width = int(self.canvas.cget("width"))

        # Calculate the width and height of the table
        table_width = self.tamanho_peca * self.colunas + 15
        table_height = self.tamanho_peca * self.linhas - 15

        # Calculate x offset to center the table horizontally
        x_offset = (canvas_width - table_width) // 2 
        y_offset = 60  # Add a margin from the top

        # Create the table rectangle at the centered top position
        self.canvas.create_rectangle(
            x_offset,
            y_offset,
            x_offset + table_width,
            y_offset + table_height,
            outline="black",
            width=5
        )
