class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hands = []
    
    def draw_cards(self, deck):
        for _ in range(14):
            card = deck.cards_pool.pop()
            self.hands.append(card)
    
    def draw_one_card(self, deck):
        card = deck.cards_pool.pop()
        self.hands.append(card)
        
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.__str__()
    

    # Other player methods



class Hand:
    def __init__(self):
        self.tiles = []

    def add_tile(self, tile):
        self.tiles.append(tile)

    # Other hand methods
