class Board:
    def __init__(self) -> None:
        self.board = []
    
    def __str__(self) -> str:
        return str(self.board)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def add_card_set(self, card_set):
        self.board.append(card_set)
        