class Checker:
    @classmethod
    def check(cls,board,player,move):
        pass
    @staticmethod
    def move_check(board,player,move):
        if IllegalMoveChecker.check(board,player,move):
            pass
        elif IllegalMoveChecker(board,player,move):
            pass
        else:
            return True
    
    @staticmethod
    def finish_check(player):
        player.score += sum([card.penalty() for card in player.hand])
