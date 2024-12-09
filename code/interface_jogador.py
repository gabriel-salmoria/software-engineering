from interface.interface import Interface
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from logic.jogo import Jogo

from tkinter import messagebox
from tkinter import simpledialog


class InterfaceJogador(DogPlayerInterface):
    def __init__(self):
        self.interface = Interface(self)
        self.nome_jogador = simpledialog.askstring(title="Nome do Jogador", prompt="Qual o seu nome?")
        self.dogActor = DogActor()
        self.estado = None

        message = self.dogActor.initialize(self.nome_jogador, self)
        messagebox.showinfo(message=message)

        self.interface.atualizar_elementos()
        self.jogo = Jogo(self, self.interface.cronometro)
        self.interface.jogo = self.jogo # cronometro precisa conseguir passar vez

        self.interface.mainloop()


    def receive_move(self, a_move):
        self.jogo.identificar_jogada(a_move)


    def start_match(self):
        status_jogo = self.jogo.receber_status_partida()

        if status_jogo == 2 or status_jogo == 3:
            return

        start_status = self.dogActor.start_match(2)
        code = start_status.get_code()
        message = start_status.get_message()

        if code == "0" or code == "1":
            messagebox.showinfo(message=message)

        elif code == "2":
            messagebox.showinfo(message=message)
            players = start_status.get_players()

            self.jogo.inicializar_jogo(players)
            self.jogo.bancoDePecas.criar_baralho()
            self.jogo.receber_estado_elementos()

            self.dogActor.send_move(self.jogo.jogada_atual)


    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)

        players = start_status.get_players()
        self.jogo.inicializar_jogo(players)


    def receive_withdrawal_notification(self):
        self.jogo.abandonar_partida()


    def reiniciar_jogo(self):
        status_jogo = self.jogo.receber_status_partida()

        if status_jogo == "2" or status_jogo == "3":
            self.jogo.reiniciar_elementos()

            self.dogActor.send_move({
                "match_status": self.jogo.status_partida,
                "tipo" : "partida reiniciada"
                })

            self.jogo.turnoAtual = True
            self.jogo.listaJogadores[0].seu_turno = True

            self.dogActor.send_move(self.jogo.jogada_atual)

InterfaceJogador()