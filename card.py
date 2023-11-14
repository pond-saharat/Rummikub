class Card:
    def __init__(self, colour, number):
        self.colour = colour
        self.number = number

    def __repr__(self):
        return f"Card({self.colour} {self.number})"
    
    @classmethod
    @property
    def wildcard(cls):
        cls.wildcard = Card("Joker", 30)