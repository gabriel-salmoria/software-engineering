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

        # Shared canvas for both Mesa and Rack
        self.canvas = tk.Canvas(
            master=self,
            width=1100,
            height=900,
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
            colunas=20,
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
            text="Clique em Mim",
            command=self.no_botao_click
        )
        self.botao.place(relx=0.95, rely=0.95, anchor="center")

        self.rack.criar_tiles()


    def no_botao_click(self) -> None:
        messagebox.showinfo("Botão Clicado", "Você clicou no botão!")
