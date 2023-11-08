import card
# import Board

NUMBER_OF_AIS = 1

class Engine:
    def __init__(self):
        # Intialize card pool and an empty board
        self.pool = card.CardPool()
        self.board = board.Board()
        # Add the players
        self.players = [HumanPlayer()]
        for num in range(NUMBER_OF_AIS):
            self.players.append(AIPlayer())
    
    def print_pool(self):
        print(self.pool)

    # def distribute(self):
    #     list_of_players = [player.HumanPlayer()]
    #     if NUMBER_OF_AIS > 0:
    #         for _ in range(NUMBER_OF_AIS):
    #             list_of_players.append(AIPlayer())

    def draw(self):
        sprites = pygame.sprite.Group()
        # Add cards in Player's hand
        for card in self.players[0].hand:
            sprites.add(card.to_sprite())
        # Add card sets and runs on a board
        # sprites.add(something)
        return sprites

a = Engine()
a.print_pool()
