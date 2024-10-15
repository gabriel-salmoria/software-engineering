from logic.piece import Piece
from interface.interface_piece import InterfacePiece


class JokerPiece(Piece):
    def __init__(
            self,
            joker_type: str,
            color: str,
        ):

        self.joker_type = joker_type
        self.number = 99
        self.color = color 

