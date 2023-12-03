from card import *

from config import *

class CardSet:
    def __init__(self, cards):
        self.cards = cards
        self.is_selected = False

    def highlight(self):
        self.is_selected = not self.is_selected
    
    def is_first_move_valid(self):
        if self.is_valid():                
            total_points = sum(card.number for card in self.cards)
            if total_points >= 30:
                return True
        else:
            return False
    
    # Create a new set of cards
    # List[Card] -> Group() or Run() or None (If they are not either Group or Run)
    @classmethod
    def create(cls, cards):
        if cls.is_group(cards):
            return Group(cards)
        elif cls.is_run(cards):
            return Run(cards)
        else:
            return None
    
    # Staticmethod: Check if the cards are valid for being classified as Group
    # List[Card] -> bool
    @staticmethod
    def is_group(cards):
        # a valid group needs at least 3 cards and there are only 4 different colours
        if len(cards) < 3 or len(cards) > NUM_OF_COLOURS:
            return False
        
        # Get the colour cards (regular cards) from a pack of cards
        colour_cards = Card.get_colour_cards(cards)   
        # a group is cards with the same number but different colours, 
        # Joker is wildcard, so only consider colour cards here
        same_num_in_hand = len(set([card.number for card in colour_cards]))
        same_clr_in_hand = len(set([card.colour for card in colour_cards]))
        if same_num_in_hand != 1:
            return False
        else:
            return same_clr_in_hand == len(colour_cards)

    # Staticmethod: Check if the cards are valid for being classified as Run
    # List[Card] -> bool
    @staticmethod
    def is_run(cards):
        # a valid run needs at least 3 cards and there are only 13 different numbers each colour
        if len(cards) < 3 or len(cards) > NUM_OF_CARDS_EACH_COLOUR // 2:
            return False
        
        # Get the colour cards (regular cards) from a pack of cards
        colour_cards = sorted(Card.get_colour_cards(cards), key=lambda x: x.number)
        # Get the count of Joker cards from a pack of cards
        joker_cards = Card.get_joker_cards(cards)

        # Check if they are all the same colour
        if not all([card.colour == colour_cards[0].colour for card in colour_cards]):
            return False

        run = []
        previous_number = None
        for card in colour_cards:
            # First iteration
            if previous_number is None:
                previous_number = card.number
                run.append(card)
                continue
            # If the current card is the previous card number + 1 -> add the card to the list
            if card.number == previous_number + 2:
                previous_number = card.number
                run.append(card)
                continue
            # If the current card is not the previous card number + 1 -> add the joker card to the list and increment the previous card number
            elif card.number != previous_number + 2: 
                while joker_cards != [] and card.number != previous_number + 2:
                    popped_joker_card = joker_cards.pop(0)
                    run.append(popped_joker_card)
                    previous_number += 2
                if joker_cards == [] and card.number != previous_number + 2:
                    print("here3",card.number, previous_number)
                    return False
            else:
                continue
        return True
    
    # Classmethod: Check if the CardSet is either a valid Group or a valid Run
    # None -> bool
    @classmethod
    def is_valid(cls,cards):
        return cls.is_group(cards) or cls.is_run(cards)              
    


class Group(CardSet):
    def __init__(self,cards):
        super().__init__(cards)
        self.group = True
        self.run = False

class Run(CardSet):
    def __init__(self,cards):
        super().__init__(cards)
        self.group = False
        self.run = True

# For testing
# is_run
# True
# cards = [ColourCard("green",1),ColourCard("green",3),ColourCard("green",5),ColourCard("green",9)] + [JokerCard()]
# print(CardSet.is_run(cards))
# cards = [ColourCard("green",1),ColourCard("green",3),ColourCard("green",5),ColourCard("green",7)] 
# print(CardSet.is_run(cards))
# cards = [ColourCard("green",1),ColourCard("green",3),ColourCard("green",9)] + [JokerCard(),JokerCard()]
# print(CardSet.is_run(cards))
# # False
# cards = [ColourCard("blue",1),ColourCard("green",3),ColourCard("green",9)] + [JokerCard(),JokerCard()]
# print(CardSet.is_run(cards))

