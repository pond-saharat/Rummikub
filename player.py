class Player:
    def __init__(self):
        self.hand = []
        self.turn = None
        self.score = 0
    def is_human(self):
        return isinstance(self,HumanPlayer)
    
    def is_ai(self):
        return isinstance(self,AIPlayer)

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

class AIPlayer(Player):
    def __init__(self):
        super().__init__()