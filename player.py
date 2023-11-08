class Player:
    def __init__(self):
        self.hand = []
        self.turn = None
        self.score = 0


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()


class AIPlayer(Player):
    def __init__(self):
        super().__init__()