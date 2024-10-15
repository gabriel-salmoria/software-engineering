import tkinter as tk
import random


# Isso aqui é só um elemento da interface, deve ser mudado de nome depois.

class InterfacePlayerFrame(tk.Frame):

    def __init__(self, master: tk.Widget, name: str):
        super().__init__(master)

        self.name = name
        self.color = random.choice(["red", "blue", "green", "orange"])
        self.create_player()


    def create_player(self) -> None:
        label = tk.Label(
            master=self,
            text=self.name,
            font=("Arial", 16)
        )
        label.pack(pady=5)

        quadrado = tk.Canvas(
            master=self,
            width=50,
            height=50,
            bg=self.color
        )
        quadrado.pack()

