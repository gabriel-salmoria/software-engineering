import tkinter as tk
from tkinter import messagebox

from interface.interface_cronometro import InterfaceCronometro
from interface.interface_frame_jogador import InterfaceFrameJogador
from interface.interface_mesa import InterfaceMesa
from interface.interface_suporte_pecas import InterfaceSuporte


class Interface(tk.Tk):
    def __init__(self, jogador_actor):
        super().__init__()
        self.title("Rummikub")
        self.geometry("1800x1000")
        self.resizable(False, False)
        self.jogadores = []
        self.jogo = None

        self.player_actor = jogador_actor

        self.create_menu_bar()
        self.criar_elementos_interface()


    def create_menu_bar(self):
        menubar = tk.Menu(self)
        menu_jogo = tk.Menu(menubar, tearoff=0)

        menu_jogo.add_command(label="Iniciar Jogo", command=self.player_actor.start_match)
        menu_jogo.add_command(label="Reiniciar Jogo", command=self.reiniciar_jogo)
        menu_jogo.add_command(label="Sair", command=self.quit)

        menubar.add_cascade(label="Jogo", menu=menu_jogo)

        self.config(menu=menubar)


    def criar_elementos_interface(self):
        self.canvas = tk.Canvas(
            master=self,
            width=1400,
            height=1000,
            bg="white"
        )
        self.canvas.pack(anchor="s")

        self.jogador_frame = tk.Frame(master=self)
        self.jogador_frame.place(relx=0.02, rely=0.2, anchor="nw")

        for i in range(2):
            jogador = InterfaceFrameJogador(master=self.jogador_frame, nome="Jogador 1")
            jogador.pack()
            self.jogadores.append(jogador)


        self.mesa_principal = InterfaceMesa(
            master=self,
            canvas=self.canvas,
            linhas=10,
            colunas=25,
            tamanho_peca=50
        )

        self.suporte_jogador = InterfaceSuporte(
            master=self,
            interface=self,
            canvas=self.canvas,
            linhas=5,
            colunas=10,
            tamanho_peca=50
        )
        self.suporte_jogador.criar_pecas()

        self.cronometro = InterfaceCronometro(
            master=self,
            tempo_maximo=60
        )
        self.cronometro.place(relx=0.5, y=20, anchor="center")

        self.botao= tk.Button(
            master=self,
            text="Passar vez / Comprar Peça",
            command=self.passar_vez
        )
        self.botao.place(relx=0.95, rely=0.95, anchor="center")


    def atualizar_elementos(self):
        pecas_mesa = self.mesa_principal.pecas
        qtd_pecas_mesa = len(pecas_mesa)

        pecas_suporte = self.suporte_jogador.pecas
        qtd_pecas_suporte = len(pecas_suporte)

        for i in range(qtd_pecas_mesa):
            pecas_mesa[i].place()

        for i in range(qtd_pecas_suporte):
            pecas_suporte[i].place()

    def reiniciar_jogo(self):
        self.jogo.reiniciar_jogo

    def passar_vez(self):
        self.jogo.listaJogadores[0].passar_vez()
