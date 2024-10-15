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



class InterfaceChronometer(tk.Label):
    def __init__(self, master: tk.Tk, max_time: int):
        super().__init__(
            master=master,
            text=f"Tempo: {max_time}",
            font=("Arial", 18),
            bg="white",
            borderwidth=2,
            relief="solid"
        )

        self.master = master
        self.max_time = max_time
        self.curr_time = max_time

        self.pack(pady=10)

        # Inicializa a contagem até zero.
        self.update_clock()


    def update_clock(self) -> None:
        if self.curr_time > 0:
            self.config(text=f"Tempo: {self.curr_time}")
            self.curr_time -= 1
            self.after(1000, self.update_clock)
        else:
            self.config(text="Tempo: 0")
            messagebox.showinfo("Tempo Acabou!", "Cronômetro chegou a zero")

            self.curr_time = self.max_time
            self.update_clock()

