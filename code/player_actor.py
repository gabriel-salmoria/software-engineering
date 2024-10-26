from interface.interface import Interface
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

from tkinter import messagebox
from tkinter import simpledialog


class JogadorActor(DogPlayerInterface):
    def __init__(self):
        self.interface = Interface(self)
        self.nome_jogador = simpledialog.askstring(title="Nome do Jogador", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(self.nome_jogador, self)
        messagebox.showinfo(message=message)
        self.interface.atualizar_elementos()
        self.interface.mainloop()

    def start_match(self):
        start_status = self.dog_server_interface.start_match(2)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        self.dog_server_interface.send_move({'nome_jogador':self.nome_jogador})

    def start_game(self):
        print('hello')

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        print(type(message))

        jogador2 = self.dog_server_interface.receive_move('nome_jogador')
        print(jogador2)

    def receive_withdrawal_notification(self):
        pass

JogadorActor()
