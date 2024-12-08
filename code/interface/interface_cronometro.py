import tkinter as tk
from tkinter import messagebox


# Descrição:
#       O Cronômetro (tk.Label) que exibe o tempo restante do jogador. 
#       Fica no centro-cima da tela. Este deve ser exibido para *todos* 
#       os jogadores.
#
# Interações:
#       É criado pela interface, tendo a mesma como master. Deve ser resetado
#       toda vez que o jogador faz um movimento.
#
# Notas:
#   --- Utiliza o método `after` do tk.Label para atualizar o tempo de forma 
#       assíncrona e manter a interface responsiva.



class InterfaceCronometro(tk.Label):
    def __init__(self, master: tk.Tk, tempo_maximo: int):
        super().__init__(
            master=master,
            text=f"Tempo: {tempo_maximo}",
            font=("Arial", 18),
            bg="white",
            borderwidth=2,
            relief="solid"
        )

        self.master = master
        self.tempo_maximo = tempo_maximo
        self.tempo_atual = tempo_maximo
        self.jogo = None

        self.pack(pady=10)


    def iniciar_cronometro(self):
        self.tempo_atual = self.tempo_maximo
        self.config(text=f"Tempo: {self.tempo_maximo}")

        self.atualizar_cronometro()


    def atualizar_cronometro(self) -> None:
        if self.jogo.turnoAtual:
            if self.tempo_atual > 0:
                self.config(text=f"Tempo: {self.tempo_atual}")
                self.tempo_atual -= 1
                self.after(1000, self.atualizar_cronometro)

            else:
                self.config(text="Tempo: 0")
                self.jogo.listaJogadores[0].passar_vez()

        else:
            self.config(text=f"Tempo: {self.tempo_maximo}")

