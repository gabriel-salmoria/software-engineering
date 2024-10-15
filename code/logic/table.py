from logic.number_piece import NumberPiece
from logic.joker_piece import JokerPiece

class Table:
    def __init__(
            self,
            rows: int,
            columns: int,
         ):
        self.rows = rows
        self.columns = columns
        self.pieces = [[None for _ in range(columns)] for _ in range(rows)]


    def check_table(self):
        """ Checks all rows in the table for valid sequences. """
        for row in range(self.rows):
            current_sequence = []

            for col in range(self.columns):

                piece = self.pieces[row][col]
                if piece is not None:
                    current_sequence.append(piece)
                else:
                    if current_sequence:
                        if not self.check_sequence(current_sequence):
                            return False
                        current_sequence = []

            if current_sequence:
                if not self.check_sequence(current_sequence):
                    return False

        return True


    def check_sequence(self, sequence: list[NumberPiece]):
        """ Checks if the given sequence is a valid run or group. """

        if len(sequence) < 3:
            return False

        if self.is_valid_run(sequence) or self.is_valid_group(sequence):
            return True

        return False


    def is_valid_run(self, sequence: list[NumberPiece]):
        """Checks if the sequence is a valid run (consecutive numbers, same color)."""

        numbers = []
        color = sequence[0].color

        for piece in sequence:
            if isinstance(piece, JokerPiece):
                numbers.append(numbers[-1]+1) 

            elif piece.get_color() != color:
                return False

            numbers.append(piece.get_number())

        for i in range(len(numbers) - 1):
            if numbers[i] + 1 != numbers[i + 1]:
                return False

        return True


    def is_valid_group(self, sequence: list[NumberPiece]):
        """Checks if the sequence is a valid group (same number, different colors)."""

        if len(sequence) > 4:
            return False

        number = sequence[0].number
        colors = set()

        for piece in sequence:
            if isinstance(piece, JokerPiece):
                continue

            elif piece.get_number() != number or piece.get_color() in colors:
                return False

            colors.add(piece.get_color())

        return True

