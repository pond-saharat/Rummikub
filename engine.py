import card
import Board

NUMBER_OF_AIS = 1
class Engine:
    def __init__(self):
        self.pool = card.cardPool()
        self.board = board.Board()
    
    def distribute(self):
        list_of_players = [player.HumanPlayer()]
        if NUMBER_OF_AIS > 0:
            for _ in range(NUMBER_OF_AIS):
                list_of_players.append(AIPlayer())
        