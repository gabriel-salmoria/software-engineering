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


class InterfacePiece(tk.Label):
    def __init__(
            self,
            master,
            parent,
            interface,
            piece,
            number: int,
            size: int,
            row: int,
            column: int,
         ):

        super().__init__(
            master=master,
            text=number,
            bg=piece.color,
            borderwidth=1,
            relief="solid",
            font=("Arial", 24),
            highlightbackground="black",
            highlightthickness=2
        )

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.size = size
        self.row = row
        self.column = column

        self.parent = parent
        self.interface = interface

        self.start_x = 0
        self.start_y = 0
        self.piece = piece

        self.place(
            x=column * size + 10,
            y=row * size + 10,
            width=size,
            height=size
        )



    def on_click(self, event: tk.Event) -> None:
        self.start_x = event.x
        self.start_y = event.y



    def on_drag(self, event: tk.Event) -> None:
        x = self.winfo_x() - self.start_x + event.x
        y = self.winfo_y() - self.start_y + event.y

        self.place(x=x, y=y)
        self.lift()



    def on_release(self, event: tk.Event) -> None:
        x, y = self.winfo_x(), self.winfo_y()

        new_parent = self.detect_new_parent(x, y)

        if new_parent is None or self.verify_collision(new_parent):
            self.place(
                x=self.column * self.size + self.parent.offset[0],
                y=self.row * self.size + self.parent.offset[1]
            )

            return

        self.parent.tiles.remove(self)
        self.parent = new_parent
        self.parent.tiles.append(self)

        closest_column = round((self.winfo_x() - 10) / self.size)
        closest_row = round((self.winfo_y() - 10) / self.size)

        new_x = closest_column * self.size + 10
        new_y = closest_row * self.size + 10

        self.place(x=new_x - 10, y=new_y + 15)
        self.row, self.column = closest_row, closest_column



    def verify_collision(self, new_parent) -> bool:
        """ Verify if the current tile has been placed into another tile. """

        tiles = new_parent.tiles

        closest_column= round((self.winfo_x() - 10) / self.size)
        closest_row = round((self.winfo_y() - 10) / self.size)

        for tile in tiles:
            if tile != self:
                if tile.row == closest_row and tile.column == closest_column:
                    return True

        return False


    def detect_new_parent(self, x: int, y: int):
        """ Detect if the tile has been placed inside a correct area. """

        table_bounds = self.interface.main_table.rect_bounds
        rack_bounds = self.interface.player_rack.rect_bounds

        if (table_bounds[0] <= x <= table_bounds[2]) and (table_bounds[1] <= y <= table_bounds[3]):
            return self.interface.main_table

        elif (rack_bounds[0] <= x <= rack_bounds[2]) and (rack_bounds[1] <= y <= rack_bounds[3]):
            return self.interface.player_rack

        return None
