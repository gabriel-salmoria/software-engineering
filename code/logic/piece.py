from interface.interface_piece import InterfacePiece
from logic.table import Table

class Piece:
    def __init__(
            self,
            piece: InterfacePiece,
            table: Table
        ):

        self.interface_peca = piece
        self.table = table

    def update_position(self, x: int, y: int) -> None:
        pass


