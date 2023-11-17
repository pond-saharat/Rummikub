import card

class Board:
    def __init__(self) -> None:
        self.board = []
    
    def __str__(self) -> str:
        return str(self.board)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    '''
    Actually, I don't think player can add a single card in boards, 
    even if it happened, it should be better if it is also a list with only one card object.
    '''
    # Add a card or cards to the board
    # List[Card] or Card -> None
    def add_cards(self, cards):
        if isinstance(cards, list):
            self.board.extend(cards)
        elif isinstance(cards, card.Card):
            self.board.append(cards)
        else:
            raise TypeError("Argument cards must be a list or a Card instance")
    
    def add_one_card_set(self, card_set):
        self.board.append(card_set)
        
    def add_all_card_sets(self, card_sets):
        self.board.extend(card_sets)
        
    def add_card_set_with_num(self, card_set, num):
        if num < len(self.board):
            self.board[num].extend(card_set)
            return True
        elif num == len(self.board):
            self.add_one_card_set(card_set)
            return True
        else:
            return False  