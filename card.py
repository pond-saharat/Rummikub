import  random


NUMBERS_OF_COLOUR_CARDS = 13
NUMBERS_OF_WILD_CARDS = 2
COLOURS = ("R","B","Y","G")

class CardPool:
    def __init__(self):
        self.pool = ColourCard.generate() + Wildcard.generate()
        random.shuffle(self.pool)

    def __str__(self):
        return " ".join(map(lambda card: card.__str__(),self.pool))


class Card:
    def __init__(self,number,colour):
        self.number = number
        self.colour = colour

    def __str__(self):
        return f"({self.colour},{self.number})"

    def __card__(self,another_card):
        return  self.number == another_card.number and self.colour == another.colour


class ColourCard(Card):
    def __init__(self,colour,number):
        super().__init__(colour,number)
    
    def penalty():
        return -self.number

    @classmethod
    def generate(cls):
        return [ColourCard(colour,card) for colour in COLOURS for card in range(1,NUMBERS_OF_COLOUR_CARDS+1)]

class Wildcard(Card):
    def __init__(self):
        super().__init__(None,"Wildcard")

    def penalty():
        return -30

    @classmethod
    def generate(cls):
        return [Wildcard() for card in range(1,NUMBERS_OF_WILD_CARDS+1)]
