import tkinter as tk
from tkinter import messagebox

from interface.interface_chronometer import InterfaceChronometer
from interface.interface_player_frame import InterfacePlayerFrame
from interface.interface_table import InterfaceTable
from interface.interface_rack import InterfaceRack


class Interface(tk.Tk):
    def __init__(self, game, player):
        super().__init__()
        self.game = game
        self.player = player

        self.title("Rummikub")
        self.geometry("1800x1000")
        self.resizable(False, False)

        self.create_menu_bar()
        self.initialize_elements()



    def create_menu_bar(self):
        menubar = tk.Menu(self)
        game_menu = tk.Menu(menubar, tearoff=0)

        game_menu.add_command(label="Iniciar Jogo", command=self.initialize_game)
        game_menu.add_command(label="Reiniciar Jogo", command=self.restart_game)
        game_menu.add_command(label="Sair", command=self.quit)

        menubar.add_cascade(label="Jogo", menu=game_menu)

        self.config(menu=menubar)


    def initialize_elements(self):

        self.canvas = tk.Canvas(
            master=self,
            width=1400,
            height=1000,
            bg="white"
        )
        self.canvas.pack(anchor="s")

        self.player_frame = tk.Frame(master=self)
        self.player_frame.place(relx=0.02, rely=0.2, anchor="nw")

        player1 = InterfacePlayerFrame(master=self.player_frame, name="Jogador 1")
        player1.pack(pady=10)

        player2= InterfacePlayerFrame(master=self.player_frame, name="Jogador 2")
        player2.pack(pady=10)

        self.main_table = InterfaceTable(
            master=self,
            canvas=self.canvas,
            rows=10,
            columns=25,
            piece_size=50
        )

        self.player_rack = InterfaceRack(
            master=self,
            interface=self,
            canvas=self.canvas,
            rows=5,
            columns=10,
            piece_size=50
        )
        self.player_rack.create_pieces(self.player.pieces)

        self.chronometer = InterfaceChronometer(
            master=self,
            max_time=60
        )
        self.chronometer.place(relx=0.5, y=20, anchor="center")

        self.button= tk.Button(
            master=self,
            text="Passar vez / Comprar Peça",
            command=self.button_click
        )
        self.button.place(relx=0.95, rely=0.95, anchor="center")


    def initialize_game(self) -> None:
        messagebox.showinfo("Iniciar Jogo", "O jogo vai começar!")


    def button_click(self) -> None:
        messagebox.showinfo("Botão Clicado", "Você clicou no botão!")


    def restart_game(self) -> None:
        messagebox.showinfo("Reiniciar Jogo", "O jogo será reiniciado!")
