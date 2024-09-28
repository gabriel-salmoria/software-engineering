import tkinter as tk
import random


# Isso aqui é só um elemento da interface, deve ser mudado de nome depois.

class Jogador(tk.Frame):
    def __init__(self, master: tk.Widget, nome: str):
        super().__init__(master)
        self.nome = nome
        self.cor = random.choice(["red", "blue", "green", "orange"])
        self.criar_jogador()

    def criar_jogador(self) -> None:
        label = tk.Label(
            master=self,
            text=self.nome,
            font=("Arial", 16)
        )
        label.pack(pady=5)

        quadrado = tk.Canvas(
            master=self,
            width=50,
            height=50,
            bg=self.cor
        )
        quadrado.pack()

