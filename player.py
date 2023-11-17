class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hands = []
        self.selected_cards = []
        self.first_moved = False
    
    def draw_cards(self, deck):
        for _ in range(14):
            card = deck.deck.pop()
            self.hands.append(card)
    
    def draw_one_card(self, deck):
        card = deck.deck.pop()
        self.hands.append(card)
        
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.__str__()

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

class AIPlayer(Player):
    def __init__(self):
        super().__init__()
