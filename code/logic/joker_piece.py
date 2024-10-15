from logic.piece import Piece
from interface.interface_piece import InterfacePiece


class JokerPiece(Piece):
    def __init__(
            self,
            piece: InterfacePiece,
            table,
            type = str,
            color = str,
        ):
        super().__init__(piece, table)

        self.type = type
        self.color = color 

