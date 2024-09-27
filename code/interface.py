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
        self.geometry("1200x800")
        self.resizable(False, False)

        self.cronometro = Cronometro(master=self, tempo_contagem=30)
        self.cronometro.place(relx=0.5, y=20, anchor="center")

        # Criar seções de jogadores na parte esquerda da tela
        self.player_frame = tk.Frame(master=self)
        self.player_frame.place(relx=0.02, rely=0.2, anchor="nw")

        jogador1 = Jogador(master=self.player_frame, nome="Jogador 1")
        jogador1.pack(pady=10)

        jogador2 = Jogador(master=self.player_frame, nome="Jogador 2")
        jogador2.pack(pady=10)

        self.mesa_principal = Mesa(
            master=self,
            linhas=10,
            colunas=20,
            tamanho_tile=50
        )
        self.mesa_principal.pack(pady=(50, 0))

        self.rack = Rack(
            master=self,
            linhas=5,
            colunas=10,
            tamanho_tile=50
        )
        self.rack.pack(side=tk.BOTTOM, pady=10)

        self.botao = tk.Button(
            master=self,
            text="Clique em Mim",
            command=self.no_botao_click
        )
        self.botao.place(relx=0.95, rely=0.95, anchor="center")


    def no_botao_click(self) -> None:
        messagebox.showinfo("Botão Clicado", "Você clicou no botão!")


