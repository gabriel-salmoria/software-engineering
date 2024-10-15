from interface.interface import Interface

from logic.deck import Deck
from logic.table import Table
from logic.player import Player

class Game:
    def __init__(self):
        self.Table = Table(
            rows=10,
            columns=25,
        )

        self.deck = Deck()
        self.player = Player(self)

        self.interface = Interface(self, self.player)
        self.interface.mainloop()
