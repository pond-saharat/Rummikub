import itertools
import deck
import board
import player
import card

from config import *

class GameEngine:
    def __init__(self, game_ui) -> None:
        # Initialize the ui engine, deck, and board
        self.deck = deck.Deck()
        self.board = board.Board()
        self.game_ui = game_ui
        # List of players
        self.players = [player.HumanPlayer() for _ in NUM_OF_HUMAN_PLAYERS] + [player.AIPlayer() for _ in NUM_OF_AI_PLAYERS]
        # Using itertools.cycle() to infinitely loop over the player list
        # Go to the next turn by calling self.next_turn()
        self._player_iterator = itertools.cycle(self.players)
        self.turn = next(self._player_iterator)
    
    # Go to the next turn
    # None -> Player
    def next_turn(self):
        self.turn = next(self._player_iterator)
        return self.turn
    
    # find every possible valid combinations of selected cards, but not effective for every case,
    # actually there can be too many kinds of different combinations given same cards, it is not sensible  
    # to let the program find all combinations, we choose another implementation method.
    # so don't need this anymore, cuz the information of grouping the cards should be given
    def find_combinations(self, cards):
        combinations = []
        cards.sort(key=lambda card: card.number)
        print(cards)
        for i in range(len(cards)):
            for j in range(i, len(cards)):
                cards_temp = cards[i:j]
                cards_left = cards[0:i] + cards[j:]
                if self.is_valid(cards_temp) and self.is_valid(cards_left):
                    combinations.append(cards_temp)
                    combinations.append(cards_left)
        return combinations        
    
    # check is_first_move_valid here, every player has to make the valid first move before regular move
    def first_move(self, player, card_sets) -> bool:
        # check input cards are in this player's hands and the card sets are valid combinations
        if all(card in player.hands for card_set in card_sets for card in card_set) \
            and all(self.is_first_move_valid(card_set) for card_set in card_sets):
                player.hands = [card for card in player.hands if card not in card_set for card_set in card_sets]
                self.board.add_all_card_sets(card_sets)
                # mark for player has made the first move
                player.first_moved = True
                print('move success')
                
                return True
        else:
            print("move failed")
            return False
    
    # card sets, corresponding nums in board
    def regular_move(self, player, card_sets, sets_nums_in_board) -> bool:
        if all(card in player.hands for card_set in card_sets for card in card_set) \
            and len(card_sets) == len(sets_nums_in_board):
            if all(self.is_valid(self.board.board[i].extend(card_sets[i])) for i in range(len(card_sets))):
                for i in range(len(card_sets)):
                    self.board.add_card_set_with_num(card_sets[i], sets_nums_in_board[i])
                
                return True
            else:
                return False
        return False
