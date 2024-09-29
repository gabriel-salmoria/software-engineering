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
    def __init__(self, master: tk.Tk, tempo_contagem: int):
        super().__init__(
            master=master,
            text=f"Tempo: {tempo_contagem}",
            font=("Arial", 18),
            bg="white",
            borderwidth=2,
            relief="solid"
        )

        self.master = master
        self.tempo_contagem = tempo_contagem
        self.pack(pady=10)

        # Inicializa a contagem até zero.
        self.atualizar_relogio()


    def atualizar_relogio(self) -> None:
        if self.tempo_contagem > 0:
            self.config(text=f"Tempo: {self.tempo_contagem}")
            self.tempo_contagem -= 1
            self.after(1000, self.atualizar_relogio)
        else:
            self.config(text="Tempo: 0")
            messagebox.showinfo("Tempo Acabou!", "Cronômetro chegou a zero")

