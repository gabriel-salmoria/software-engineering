import tkinter as tk
from tkinter import messagebox

from cronometro import Cronometro
from jogador import Jogador
from mesa import Mesa
from rack import Rack


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rummikub")
        self.geometry("1500x800")
        self.resizable(False, False)

        # Create the menu bar
        self.create_menu_bar()

        # Shared canvas for both Mesa and Rack
        self.canvas = tk.Canvas(
            master=self,
            width=1400,
            height=1000,
            bg="white"
        )
        self.canvas.pack(anchor="s")

        # Criar seções de jogadores na parte esquerda da tela
        self.player_frame = tk.Frame(master=self)
        self.player_frame.place(relx=0.02, rely=0.2, anchor="nw")

        jogador1 = Jogador(master=self.player_frame, nome="Jogador 1")
        jogador1.pack(pady=10)

        jogador2 = Jogador(master=self.player_frame, nome="Jogador 2")
        jogador2.pack(pady=10)

        # Create Mesa and Rack within the shared canvas
        self.mesa_principal = Mesa(
            master=self,
            canvas=self.canvas,
            linhas=10,
            colunas=25,
            tamanho_tile=50
        )

        self.rack = Rack(
            master=self,
            canvas=self.canvas,
            linhas=5,
            colunas=10,
            tamanho_tile=50,
            interface=self
        )

        self.cronometro = Cronometro(
            master=self,
            tempo_contagem=30
        )
        self.cronometro.place(relx=0.5, y=20, anchor="center")

        self.botao = tk.Button(
            master=self,
            text="Passar vez/Comprar Carta",
            command=self.no_botao_click
        )
        self.botao.place(relx=0.95, rely=0.95, anchor="center")

        self.rack.criar_tiles()


    def create_menu_bar(self):
        # Create a menubar
        menubar = tk.Menu(self)

        # Create the Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Iniciar Jogo", command=self.iniciar_jogo)
        game_menu.add_command(label="Reiniciar Jogo", command=self.reiniciar)

        game_menu.add_command(label="Sair", command=self.quit)

        # Add the Game menu to the menubar
        menubar.add_cascade(label="Jogo", menu=game_menu)

        # Attach the menubar to the window
        self.config(menu=menubar)

    def iniciar_jogo(self):
        # Logic to start the game can be placed here
        messagebox.showinfo("Iniciar Jogo", "O jogo vai começar!")

    def no_botao_click(self) -> None:
        messagebox.showinfo("Botão Clicado", "Você clicou no botão!")

    def reiniciar(self):
        pass


if __name__ == "__main__":
    app = Interface()
    app.mainloop()
