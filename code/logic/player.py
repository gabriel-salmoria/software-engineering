

class Player:
    def __init__(self, game):
        self.game = game
        self.pieces = self.get_pieces()

        self.won = False
        self.turn = False

    def get_pieces(self) -> list:
        pieces = []

        for _ in range(14):
            piece = self.game.deck.get_piece()
            pieces.append(piece)

        return pieces

    def check_victory(self) -> bool:
        return len(self.pieces) == 0
