import random
from logic.number_piece import NumberPiece
from logic.joker_piece import JokerPiece 



class Deck:
    def __init__(self):
        self.pieces = self.initialize_deck()


    def initialize_deck(self) -> list:
        pieces = []
        colors = ["lightblue", "lightgreen", "lightcoral", "lightyellow"]

        for number in range(1,13):
            for color in colors:
                piece = NumberPiece(number=number, color=color)
                pieces.append(piece)

        for color in colors:
            piece = JokerPiece(joker_type='normal', color=color)
            pieces.append(piece) 

        return pieces


    def get_piece(self):
        piece = random.choice(self.pieces)
        self.pieces.remove(piece)

        return piece





