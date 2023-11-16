import card

from config import *

class Set:
    def __init__(self,cards):
        self.cards = cards

    # Create a new set of cards
    # List[Card] -> Group() or Run() or False (If they are not either Group or Run)
    @classmethod
    def create(cls, cards):
        if cls.is_group(cards):
            return Group(cards)
        elif cls.is_run(cards):
            return Run(cards)
        else:
            return False
    # Check if the cards are valid for being classified as Group
    # List[Card] -> bool
    @staticmethod
    def is_group(cards):
        # Need comments
        if len(cards) < 3:
            return False
        # Get the colour cards from a pack of cards
        colour_cards = card.Card.get_colour_cards(cards)   
        # Need comments
        if len(set([card.number for card in colour_cards])) != 1:
            return False
        else:
            return len(set([card.colour for card in colour_cards])) == len(colour_cards)

    # Check if the cards are valid for being classified as Run
    # List[Card] -> bool
    @staticmethod
    def is_run(cards):
        # Need comments
        if len(cards) < 3:
            return False
        # Need comments
        colour_cards = Card.get_colour_cards(cards)
        joker_cards_count = len(card.Card.get_joker_cards(cards)) #len([card for card in cards if card.number == 30]) 
        # Need comments
        if len(set([card.colour for card in colour_cards])) != 1:
            return False
        else:
            list_of_numbers = sorted([card.number for card in colour_cards])
            for i in range(1, len(list_of_numbers)):
                if list_of_numbers[i] != list_of_numbers[i-1] + 1:
                    if joker_cards_count == 0:
                        return False
                    joker_cards_count -= 1
            return True
    
    # Check if the set is either a valid Group or a valid Run
    # None -> bool
    def is_valid(self, cards):
        return self.is_group(cards) or self.is_run(cards)              
    
    def is_first_move_valid(self, cards):
        if self.is_valid(cards):                
            total_points = sum(card.number for card in cards)
            if total_points >= 30:
                return True
        else:
            return False
class Group(Set):
    def __init__(self,cards):
        super().__init__(cards)
        self.group = True
        self.run = False

class Run(Set):
    def __init__(self,cards):
        super().__init__(cards)
        self.group = False
        self.run = True