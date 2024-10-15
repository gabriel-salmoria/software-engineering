from logic.piece import Piece
from interface.interface_piece import InterfacePiece

class NumberPiece(Piece):
    def __init__(
            self,
            piece: InterfacePiece,
            table,
            number: int,
            color: str,
        ):
        super().__init__(piece, table)

        self.number = number
        self.color = color


    def get_color(self):
        return self.color


    def get_number(self):
        return self.number

