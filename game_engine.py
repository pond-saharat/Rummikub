import itertools
import deck
import board
import player
import cardset
import pygame
import card as c
import button
import timer as t
import bot

from config import *


class GameEngine:
    def __init__(self, game_ui) -> None:
        # Initialize the ui engine, deck, and board
        self.deck = deck.Deck()
        self.objects = None
        
        # self.board = board.Board()
        self.hand_regions = []
        self.game_ui = game_ui
        self.screen = self.game_ui.screen
        # List of players
        self.players = [
            player.HumanPlayer(f"Human_player_{_}") for _ in range(self.game_ui.num_of_ais)
        ] + [player.AIPlayer(f"AI_player_{_}") for _ in range(self.game_ui.num_of_humans)]
        # Using itertools.cycle() to infinitely loop over the player list
        # Go to the next turn by calling self.next_turn()
        self._player_iterator = itertools.cycle(self.players)
        self.current_player = next(self._player_iterator)

        # Round
        self.round = 1
        # Game Round
        self.game_round = 1

        # deal cards to players
        self.deal_cards()
        self.num_of_cards_in_valid_cardset = 0
        # Link pygame.Rect objects to player's hand_region
        self.set_player_hand_regions()
        
        # Score and a list of winners
        self.winning_score = 0
        self.winners = []

        print(f"current player hands: {self.current_player.hands}")
        print(f"deck: {len(self.deck.deck)} cards")
        
        

    # Get all objects
    # UI and all cards
    def update_objects(self):
        # self.objects = self.deck.deck[-2:0] # NEED TO EDIT THE VALUE THIS IS FOR TESTING
        # self.objects = self.deck.deck + self.board.board + self.current_player.hands
        # print(f"deck: {len(self.deck.deck)}")
        self.objects = self.deck.deck + [card for player in self.players for card in player.hands]
        self.objects += self.game_ui.ui_objects

    # Go to the next turn
    # None -> Player
    def next_turn(self):
        for pos, card_list in self.game_ui.grid_cards.items():
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
        
        self.game_ui.draw_button.reset()
        self.game_ui.selected_cards = []
        self.game_ui.reset_drag_parameters()
        self.game_ui.set_current_player_hands()
        self.game_ui.grid_cards =  {k: v for k, v in self.game_ui.grid_cards.items() if v != []}
        self.current_player.made_move = False
        # Unflip all cards
        c.Card.set_to_unflipped(self.current_player.hands)

        # If this player is the last player -> check if the current round is the last round
        if self.current_player == self.players[-1]:
            self.round += 1
        
        # Check if the current player is a winner
        if not self.check_win() and not self.game_round > MAX_ROUND:
            # If not -> Go to the next turn
            self.current_player = next(self._player_iterator)
            self.game_ui.timer = t.Timer()
            c.Card.set_to_flipped(self.current_player.hands)
            c.Card.set_others_to_unflipped(self)
            print(f"It's now : {self.current_player}'s turn")
            print(f"current player hands: {self.current_player.hands}")
            return self.current_player
        else:
            # If there is a winner
            self.endgame_score_calculation()
            self.game_ui.game_state = "Rummikub!"
            print(f"{self.winners} are a winner with a score of {self.winning_score}")
            # Whole game round
            self.game_round += 1
            

    def deal_cards(self):
        for player in self.players:
            player.draw_cards(self.deck)

        c.Card.set_others_to_unflipped(self)

        for card in self.deck.deck:
            card.visible = False
        
    # Link pygame.Rect objects to player's hand_region
    # None -> None
    def set_player_hand_regions(self):
        colour = (0,0,0,0)
        p1 = pygame.Rect(P1_HANDS_REGION)
        p2 = pygame.Rect(P2_HANDS_REGION)
        p3 = pygame.Rect(P3_HANDS_REGION)
        p4 = pygame.Rect(P4_HANDS_REGION)

        self.hand_regions = [p1,p2,p3,p4]
        for index, player in enumerate(self.players):
            player.hand_region = self.hand_regions[index]

    # Draw hand regions
    # None -> None  
    def draw_regions(self):
        # Draw hand regions
        colour = (40,195,233,100)
        offset = 3
        radius = 0
        self.game_ui.draw_region = pygame.Rect(DRAW_CARDS_REGION)
        regions = self.hand_regions + [self.game_ui.draw_region]
        
        for region in regions:
            shadow = pygame.Surface((region.width, region.height), pygame.SRCALPHA)
            shadow_rect = shadow.get_rect()
            pygame.draw.rect(shadow,(16, 38, 59, 100), shadow_rect, border_radius=radius)
            
            shadow_rect.x = region.x + offset
            shadow_rect.y = region.y + offset

            self.screen.blit(shadow, (shadow_rect.x, shadow_rect.y))
            pygame.draw.rect(self.screen,colour,region,border_radius=radius)
        

    # Check if the current player is a winner
    # If so, calculate the score and change game_state
    # None -> bool
    def check_win(self):
        if self.current_player.hands == []:
            self.current_player.winner = True
            return True
        else:
            return False

    # Calculate the final score of each player and set the max score and the list of winners 
    # None -> None
    def endgame_score_calculation(self):
        winners = [player for player in self.players if player.winner == True]
        winner_exists = len(winners) != 0
        if winner_exists:
            penalised_players = [player for player in self.players if player.winner == False]
            for player in penalised_players:
                penalty = c.Card.get_penalty(player.hands)
                player.score += penalty
                for winner in winners:
                    winner.score -= penalty
        else:
            # for player in self.players:
            #     player.score += c.Card.get_penalty(player.hands)
            pass
        
        # Get the list of winners and their scores
        score_to_players = {}
        for player in self.players:
            if player.score not in score_to_players:
                score_to_players[player.score] = [player]
            else:
                score_to_players[player.score].append(player)

        self.winning_score = max(list(score_to_players.keys()))
        self.winners = score_to_players[self.winning_score]
        
    # def get_num_of_cards_in_valid_cardset(self):
    #     number_of_valid_cardsets = 0
    #     if self.game_ui.grid_cards != {}:
    #         for key, cards in self.game_ui.grid_cards.items():
    #             if cardset.CardSet.is_valid(cards):
    #                 number_of_valid_cardsets += len(cards)
    #     return number_of_valid_cardsets

    
        
    
    
    
    
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
