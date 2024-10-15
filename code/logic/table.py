from logic.piece import Piece
from logic.number_piece import NumberPiece

class Table:
    def __init__(
            self,
            rows: int,
            columns: int,
            pieces: list[list[Piece]]
         ):

        self.rows = rows
        self.columns = columns
        self.pieces = pieces

    def check_sequencia(self, sequence: list[NumberPiece]):
        piece1 = sequence[0]
        piece2 = sequence[1]
        linear = (piece1.color == piece2.color) and (piece1.number == piece2.number-1)
        

