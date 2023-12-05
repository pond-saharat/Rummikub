import itertools
import deck
import board
import player
import cardset
import pygame
import card

from config import *


class GameEngine:
    def __init__(self, game_ui) -> None:
        # Initialize the ui engine, deck, and board
        self.deck = deck.Deck()
        self.objects = self.deck.deck
        # self.board = board.Board()
        self.hand_regions = []
        self.game_ui = game_ui
        self.screen = self.game_ui.screen
        # List of players
        self.players = [
            player.HumanPlayer(f"Human_player_{_}") for _ in range(NUM_OF_HUMAN_PLAYERS)
        ] + [player.AIPlayer("AI_player_{_}") for _ in range(NUM_OF_AI_PLAYERS)]
        # Using itertools.cycle() to infinitely loop over the player list
        # Go to the next turn by calling self.next_turn()
        self._player_iterator = itertools.cycle(self.players)
        self.current_player = next(self._player_iterator)
        
        # Round
        self.round = 1

        # deal cards to players
        self.deal_cards()
        
        # Link pygame.Rect objects to player's hand_region
        self.set_player_hand_regions()
        
        print(f"current player hands: {self.current_player.hands}")
        print(f"deck: {len(self.deck.deck)}")
        
        

    # Get all objects
    # UI and all cards
    def update_objects(self):
        # self.objects = self.deck.deck[-2:0] # NEED TO EDIT THE VALUE THIS IS FOR TESTING
        # self.objects = self.deck.deck + self.board.board + self.current_player.hands
        # print(f"deck: {len(self.deck.deck)}")
        self.objects = self.deck.deck + [card for player in self.players for card in player.hands]
        return self.objects

    # Go to the next turn
    # None -> Player
    def next_turn(self):
        for pos,card_list in self.game_ui.grid_cards.items():
            # print(card_list)
            # print(pos,cardset.CardSet.is_valid(card_list))
            if not cardset.CardSet.is_valid(card_list):
                # return to player's hand
                for card in card_list:
                    card.owner = self.current_player
                self.current_player.hands.extend(card_list)
                self.game_ui.grid_cards[pos] = []
                
            else:
                pass
        self.game_ui.reset_drag_parameters()
        self.game_ui.set_current_player_hands()
        self.game_ui.grid_cards =  {k: v for k, v in self.game_ui.grid_cards.items() if v != []}

        # If this player is the last player -> check if the current round is the last round
        if self.current_player == self.players[-1]:
            self.round += 1

        # Check if the current player is a winner
        if not self.check_win() and not self.round == MAX_ROUND:
            self.current_player == self.players[-1]
            self.round +=1
            # If not -> Go to the next turn
            self.current_player = next(self._player_iterator)
            print(f"It's now : {self.current_player}'s turn")
            print(f"current player hands: {self.current_player.hands}")
            return self.current_player
        else:
            # If there is a winner
            score, winners = self.endgame_score_calculation()
            self.game_ui.game_state = "congratulation"
            print(f"{winners} are a winner with a score of {score}")

    def deal_cards(self):
        for player in self.players:
            player.draw_cards(self.deck)
        
    # Link pygame.Rect objects to player's hand_region
    # None -> None
    def set_player_hand_regions(self):
        # Define hand regions
        self.hand_regions.append(pygame.draw.rect(self.screen,0,(HANDS_REGION,SCREEN_HEIGHT - HANDS_REGION,SCREEN_WIDTH - 2 * HANDS_REGION,HANDS_REGION),2))
        self.hand_regions.append(pygame.draw.rect(self.screen,0,(0, HANDS_REGION, HANDS_REGION, SCREEN_HEIGHT - 2 * HANDS_REGION),2))
        self.hand_regions.append(pygame.draw.rect(self.screen,0,(HANDS_REGION, 0, SCREEN_WIDTH - 2 * HANDS_REGION, HANDS_REGION),2))
        self.hand_regions.append(pygame.draw.rect(self.screen,0,(HANDS_REGION + BOARD_WIDTH, HANDS_REGION,HANDS_REGION,SCREEN_HEIGHT - 2 * HANDS_REGION),2))

        for player in self.players:
            player.hand_region = self.hand_regions.pop(0)

    # Check if the current player is a winner
    # If so, calculate the score and change game_state
    # None -> bool
    def check_win(self):
        if self.current_player.hands == []:
            self.current_player.winner = True
            self.score += 30
            return True
        else:
            return False

    # Calculate the final score of each player and return the tuple of the max score and the list of winners 
    # None -> Tuple(score, List[Player])
    def endgame_score_calculation(self):
        winner_exists = len([player for player in self.players if player.winner == True]) != 0
        if winner_exists:
            penalised_players = [player for player in self.players if player.winner == False]
            for player in penalised_players:
                player.score += card.Card.get_penalty(player.hands)
        else:
            for player in self.players:
                player.score += card.Card.get_penalty(player.hands)
        # Get the list of winners and their scores
        score_to_players = {}
        for player in self.players:
            if player.score not in score_to_players:
                score_to_players[player.score] = [player]
            else:
                score_to_players[player.score].append(player)
        # Return the tuple of the list of winners and their score
        max_score = max(list(score_to_players.keys()))
        return max_score, score_to_players[max_score]
        
        
    # # find every possible valid combinations of selected cards, but not effective for every case,
    # # actually there can be too many kinds of different combinations given same cards, it is not sensible
    # # to let the program find all combinations, we choose another implementation method.
    # # so don't need this anymore, cuz the information of grouping the cards should be given
    # def find_combinations(self, cards):
    #     combinations = []
    #     cards.sort(key=lambda card: card.number)
    #     # print(cards)
    #     for i in range(len(cards)):
    #         for j in range(i, len(cards)):
    #             cards_temp = cards[i:j]
    #             cards_left = cards[0:i] + cards[j:]
    #             if self.is_valid(cards_temp) and self.is_valid(cards_left):
    #                 combinations.append(cards_temp)
    #                 combinations.append(cards_left)
    #     return combinations

    # """ 
    # need to modify the function with Cardset() 
    # """

    # # check is_first_move_valid here, every player has to make the valid first move before regular move
    # def first_move(self, player, card_sets) -> bool:
    #     # check input cards are in this player's hands and the card sets are valid combinations
    #     if all(
    #         card in player.hands for card_set in card_sets for card in card_set
    #     ) and all(self.is_first_move_valid(card_set) for card_set in card_sets):
    #         player.hands = [
    #             card
    #             for card in player.hands
    #             if not any(card in card_set for card_set in card_sets)
    #         ]
    #         self.board.add_all_card_sets(card_sets)
    #         # mark for player has made the first move
    #         player.first_moved = True
    #         print("move success")

    #         return True
    #     else:
    #         print("move failed")
    #         return False

    # """ 
    # need to modify the function with Cardset() 
    # """

    # # card sets, corresponding nums in board
    # def regular_move(self, player, card_sets, sets_nums_in_board) -> bool:
    #     if player.first_moved == False:
    #         print("Please make the first move")
    #         return False
    #     # check input cards are in this player's hands and the card sets are valid combinations
    #     if all(
    #         card in player.hands for card_set in card_sets for card in card_set
    #     ) and len(card_sets) == len(sets_nums_in_board):
    #         if all(
    #             self.is_valid(self.board.board[i] + card_sets[i])
    #             for i in range(len(card_sets))
    #         ):
    #             for i in range(len(card_sets)):
    #                 player.hands = [
    #                     card
    #                     for card in player.hands
    #                     if not any(card in card_set for card_set in card_sets)
    #                 ]
    #                 self.board.add_card_set_with_num(
    #                     card_sets[i], sets_nums_in_board[i]
    #                 )
    #             print("move success")
    #             return True
    #         else:
    #             print("move failed")
    #             return False
    #     return False
