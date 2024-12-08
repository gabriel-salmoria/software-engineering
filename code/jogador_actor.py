from interface.interface import Interface
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from logic.jogo import Jogo

from tkinter import messagebox
from tkinter import simpledialog


class JogadorActor(DogPlayerInterface):
    def __init__(self):
        self.interface = Interface(self)
        self.nome_jogador = simpledialog.askstring(title="Nome do Jogador", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        self.estado = None

        message = self.dog_server_interface.initialize(self.nome_jogador, self)
        messagebox.showinfo(message=message)

        self.interface.atualizar_elementos()
        self.jogo = Jogo(self, self.interface.cronometro)
        self.interface.jogo = self.jogo # cronometro precisa conseguir passar vez

        self.interface.mainloop()


    def receive_move(self, a_move):
        self.jogo.identificar_jogada(a_move)


    # 99% de acordo com os diagramas
    def start_match(self):
        status_jogo = self.jogo.receber_status_partida()

        if status_jogo == 2 or status_jogo == 3:
            return

        start_status = self.dog_server_interface.start_match(2)
        code = start_status.get_code()
        message = start_status.get_message()

        if code == "0" or code == "1":
            messagebox.showinfo(message=message)

        elif code == "2":
            players = start_status.get_players()

            self.jogo.inicializar_jogo(players)
            self.jogo.bancoDePecas.criar_baralho()
            self.jogo.receber_estado_elementos()

            self.dog_server_interface.send_move(self.jogo.jogada_atual)


    # de acordo com os diagramas
    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)

        players = start_status.get_players()
        self.jogo.inicializar_jogo(players)
        self.interface.atualizar_elementos()


    def receive_withdrawal_notification(self):
        self.jogo.abandonar_partida()


    # inutil ainda.
    def reiniciar_jogo(self):
        status_jogo = self.jogo.receber_status_partida()

        self.jogo.reiniciar_elementos()

        self.dog_server_interface.send_move({
            "match_status": "fodase",
            "tipo" : "partida reiniciada"
            })

        self.jogo.turnoAtual = True
        self.jogo.listaJogadores[0].seu_turno = True

        self.dog_server_interface.send_move(self.jogo.jogada_atual)





JogadorActor()
