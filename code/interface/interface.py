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

        self.player_actor = jogador_actor

        self.create_menu_bar()
        self.inicializar_elementos()


    def create_menu_bar(self):
        menubar = tk.Menu(self)
        menu_jogo = tk.Menu(menubar, tearoff=0)

        menu_jogo.add_command(label="Iniciar Jogo", command=self.iniciar_jogo)
        menu_jogo.add_command(label="Reiniciar Jogo", command=self.reiniciar_jogo)
        menu_jogo.add_command(label="Sair", command=self.quit)

        menubar.add_cascade(label="Jogo", menu=menu_jogo)

        self.config(menu=menubar)


    def inicializar_elementos(self):
        self.canvas = tk.Canvas(
            master=self,
            width=1400,
            height=1000,
            bg="white"
        )
        self.canvas.pack(anchor="s")

        self.jogador_frame = tk.Frame(master=self)
        self.jogador_frame.place(relx=0.02, rely=0.2, anchor="nw")

        self.jogador1 = InterfaceFrameJogador(master=self.jogador_frame, nome="Jogador 1")
        self.jogador1.pack(pady=10)

        self.jogador2= InterfaceFrameJogador(master=self.jogador_frame, nome="Jogador 2")
        self.jogador2.pack(pady=10)

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
            command=self.botao_click
        )
        self.botao.place(relx=0.95, rely=0.95, anchor="center")


    def atualizar_elementos(self):
        self.jogador1.atualizar_nome(self.player_actor.nome_jogador)


    def iniciar_jogo(self) -> None:
        self.player_actor.start_match()


    def botao_click(self) -> None:
        messagebox.showinfo("Botão Clicado", "Você clicou no botão!")


    def reiniciar_jogo(self) -> None:
        messagebox.showinfo("Reiniciar Jogo", "O jogo será reiniciado!")
