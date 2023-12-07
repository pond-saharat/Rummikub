# Class Board
# A collection of cards of the board
class Board:
    def __init__(self) -> None:
        self.board = []
        self.grid_cards = {}
        self.selected_cards = []
    
    def __str__(self) -> str:
        return str(self.board)
    
    def __repr__(self) -> str:
        return self.__str__()
    
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