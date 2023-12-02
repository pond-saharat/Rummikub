import cardset
import card
import copy

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hands = []
        self.score = 0
        self.first_moved = False
        # This will keep record of which objects the player is currently selecting. 
        # The last index is the destination 
        # It can be only three formats: [cardset,card] or [card,card,...,card,card,cardset] or [cardset,cardset]
        self.selected_cards = []
    
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

    def make_move(self,game_engine):
        source = self.selected_cards[:-1] # This is a list
        destination = self.selected_cards[-1] # This is an instance

        # [card,card,...,card,card,cardset] or [card,cardset]
        # From hand to a board: 
        if isinstance(destination, cardset.CardSet):
            valid_source = cardset.CardSet.is_valid(source)
            valid_source_and_destination = cardset.CardSet.is_valid(source + destination)

            # User intend to create a new set of cards -> check if the new
            if len(source) > 1 and valid_source \
                and not valid_source_and_destination:
                if self.first_moved == False: 
                    if not self.make_first_move(source):
                        self.cancel_move("First move is invalid")
                        return False
                    
                created_set = cardset.CardSet.create(source)
                # Add the created set to the board
                game_engine.board.board.append(created_set)
                # Reference a parent set of each card
                for card in created_set.cards:
                    card.parent_set = created_set

            # User just intend to add a card to an existing set of cards
            elif len(source) == 1 and cardset.CardSet.is_valid(source+destination.cards):
                # Create one set
                tmp = cardset.CardSet.create(source+destination.cards)
                # Use that set's cards as the current set's cards
                destination.cards = tmp.cards
        
        # Destroy a set: [cardset,card]
        elif len(source) == 1 and isinstance(source[0], cardset.CardSet) and isinstance(destination, card.Card):
            # Retrive the cards back
            self.hands.extend(destination.cards)
            # Remove the set from the board
            try:
                game_engine.board.board.remove(destination)
            except Exception as e:
                print(e)
        else:
            # Don't know user's intention
            self.cancel_move("Don't know user's intention")
            pass
<<<<<<< HEAD
    
=======

    # Make first move
    # None -> None
    def make_first_move(self, source):
        sum_of_cards = 0
        for card in source:
            if card.number and isinstance(card, card.ColourCard):
                sum_of_cards += card.number
        return sunm

>>>>>>> 759198a09780b933107918013607d1f65403956c
    # Cancel the current move
    def cancel_move(self,reason=None):   
        print(f"IllegalMove: {reason}")
        pass

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
