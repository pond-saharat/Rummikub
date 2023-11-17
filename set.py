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
        # a valid group needs at least 3 cards and there are only 4 different colours
        if len(cards) < 3 or len(cards) > NUM_OF_COLOURS:
            return False
        
        # Get the colour cards (regular cards) from a pack of cards
        colour_cards = card.Card.get_colour_cards(cards)   
        # a group is cards with the same number but different colours, 
        # Joker is wildcard, so only consider colour cards here
        same_num_in_hand = len(set([card.number for card in colour_cards]))
        same_clr_in_hand = len(set([card.colour for card in colour_cards]))
        if same_num_in_hand != 1:
            return False
        else:
            return same_clr_in_hand == len(colour_cards)

    # Check if the cards are valid for being classified as Run
    # List[Card] -> bool
    @staticmethod
    def is_run(cards):
        # a valid run needs at least 3 cards and there are only 13 different numbers each colour
        if len(cards) < 3 or len(cards) > NUM_OF_CARDS_EACH_COLOUR:
            return False
        
        # Get the colour cards (regular cards) from a pack of cards
        colour_cards = card.Card.get_colour_cards(cards)
        # Get the count of Joker cards from a pack of cards
        joker_cards_count = len(card.Card.get_joker_cards(cards)) #len([card for card in cards if card.number == 30]) 
        # a run needs same colour for colour/regular cards
        if len(set([card.colour for card in colour_cards])) != 1:
            return False
        else:
            list_of_numbers = sorted([card.number for card in colour_cards])
            # numbers should be sequence unless there are enough Joker cards in hands
            for i in range(1, len(list_of_numbers)):
                if list_of_numbers[i] != list_of_numbers[i-1] + 1:
                    if joker_cards_count == 0:
                        return False
                    # each time there is a gap between adjacent numbers, the count of Joker cards will decrease by 1
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