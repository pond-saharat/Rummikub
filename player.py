import cardset
import card
import copy
import bot
from config import *
import pygame

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
        self.hand_region = None # pygame.Rect
        # Track if this person is a winner or not
        self.winner = False
        self.made_move = False
        self.hand_region = [P1_HANDS_REGION, P2_HANDS_REGION, P3_HANDS_REGION, P4_HANDS_REGION][int(self.name[-1])]
        
    def draw_cards(self, deck):
        popped_to_hand = deck.deck[:14]
        for card in popped_to_hand:
            card.owner = self
        self.hands += popped_to_hand
        deck.deck = deck.deck[14:]
    
    def draw_one_card(self, game_ui):
        deck = game_ui.game_engine.deck.deck
        if len(deck) == 0:
            game_ui.notification = "Deck is empty"
            return
        
        game_ui.draw_button.left_click_action(game_ui)
        card1 = game_ui.draw_button.cards[0]
        
        # default: choose the first card
        card1.owner = self
        card1.is_selected = True
        
        # dest_xy_1 = (self.hand_region[0] + self.hand_region[2] //2, self.hand_region[1] + self.hand_region[3]//2) 
        dest_xy =  game_ui.find_hands_destination([card1], game_ui.game_engine.current_player)
        
        # # drag the cards to the grid
        # game_ui.move_cards_animation([card1], [dest_xy_1])
        game_ui.move_cards_animation([card1], dest_xy)
        
        # self.hands.append(card1)
        game_ui.game_engine.current_player.hands.append(card1)
        
        game_ui.draw_button.cards.remove(card1)
        deck.remove(card1)
        # card1.visible = False
        game_ui.draw_button.reset()
        game_ui.game_engine.current_player.made_move = True
        
        
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.__str__()


    def make_first_move(self, game_ui):
        # Find the best combos
        self.hand_cards_tensor = bot.CardsTensor(cards=self.hands)
        best_play_idx_combos, max_sum = self.hand_cards_tensor.find_max_sum_combos_idx()

        all_indices = [i for combo in best_play_idx_combos for i in combo]
        cards_in_best_play = [self.hands[i] for i in all_indices]
        self.selected_cards = cards_in_best_play
        
        # # Select the cards
        # for idx in all_indices:
        #     self.selected_cards.append(self.hands[idx])
        
        game_ui.notification = f"{cards_in_best_play} {max_sum}"
        
        return cards_in_best_play
    
    
    
    
    
    # def make_move(self,game_engine):
    #     source = self.selected_cards[:-1] # This is a list
    #     destination = self.selected_cards[-1] # This is an instance

    #     # [card,card,...,card,card,cardset] or [card,cardset]
    #     # From hand to a board: 
    #     if isinstance(destination, cardset.CardSet):
    #         valid_source = cardset.CardSet.is_valid(source)
    #         valid_source_and_destination = cardset.CardSet.is_valid(source + destination)

    #         # User intend to create a new set of cards -> check if the new
    #         if len(source) > 1 and valid_source \
    #             and not valid_source_and_destination:
    #             created_set = cardset.CardSet.create(source)
    #             # Add the created set to the board
    #             game_engine.board.board.append(created_set)
    #             # Reference a parent set of each card
    #             for card in created_set.cards:
    #                 card.parent_set = created_set

    #         # User just intend to add a card to an existing set of cards
    #         elif len(source) == 1 and cardset.CardSet.is_valid(source+destination.cards):
    #             # Create one set
    #             tmp = cardset.CardSet.create(source+destination.cards)
    #             # Use that set's cards as the current set's cards
    #             destination.cards = tmp.cards
        
    #     # Destroy a set: [cardset,card]
    #     elif len(source) == 1 and isinstance(source[0], cardset.CardSet) and isinstance(destination, card.Card):
    #         # Retrive the cards back
    #         self.hands.extend(destination.cards)
    #         # Remove the set from the board
    #         try:
    #             game_engine.board.board.remove(destination)
    #         except Exception as e:
    #             print(e)
    #     else:
    #         # Don't know user's intention
    #         self.cancel_move("Don't know user's intention")
    #         pass
    
    # # Cancel the current move
    # def cancel_move(self,reason=None):   
    #     print(f"IllegalMove: {reason}")
    #     pass

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

class AIPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        
    def make_first_move(self):
        # Find the best combos
        self.card_tensor = bot.CardsTensor(cards=self.hands)
        best_play = self.card_tensor.find_longest_combos()
        for combo in best_play[0]:
            self.selected_cards.extend(combo.tensor2cards())
        
        
        # # Add the best set to the board
        # game_engine.board.board.append(best_set)
        # # Remove the cards from the player's hand
        # for card in best_set.cards:
        #     self.hands.remove(card)
        # # Set the first moved flag to True
        # self.first_moved = True
