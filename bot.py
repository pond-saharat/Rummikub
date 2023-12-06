import card
import deck
import itertools
from config import *

import numpy as np

# Wrapping ndarray 
class CardsTensor():
    def __init__(self, tensor=None, cards=None):
        self.colorText2Num_dict = {'Red': 0, 'Green': 1, 'Blue': 2, 'Yellow': 3, 'Pink': 4, 'Joker': 5}
        self.colorNum2Text_dict = {0: 'Red', 1: 'Green', 2: 'Blue', 3: 'Yellow', 4: 'Pink', 5: 'Joker'}
        self.colour_num = 5
        self.number_num = 15
        if tensor is not None:
            self.tensor = tensor
            self.cards = self.tensor2cards()
        elif cards is not None:
            self.tensor = self.cards2tensor(cards)
            self.cards = cards
        else:
            self.tensor = np.zeros((15, 6, 2))
            self.cards = []
        
        self.cards_idx_dict = {}    # {(card.colour, card.number, 0): idx1, ...]}
        if cards is not None:
            for i, c in enumerate(cards):
                if (c.colour, c.number, 0) not in self.cards_idx_dict:
                    self.cards_idx_dict[(c.colour, c.number, 0)] = i
                else:
                    self.cards_idx_dict[(c.colour, c.number, 1)] = i

    def cards2tensor(self, cards_from_deck):
        cards_from_deck = [card for card in cards_from_deck if card.number is not None]
        cards_tensor = np.zeros((15, 6, 2))
        for c in cards_from_deck:
            if c.number is None:    # Joker
                color = self.colorText2Num_dict[c.colour]
                for num in range(15):
                    if cards_tensor[num][color][0] == 0:
                        cards_tensor[num][color][0] = 1
                    elif cards_tensor[num][color][0] == 1:
                        cards_tensor[num][color][1] = 1
            else:
                num = int(c.number) - 1
                color = self.colorText2Num_dict[c.colour]
                if cards_tensor[num][color][0] == 0:
                    cards_tensor[num][color][0] = 1
                elif cards_tensor[num][color][0] == 1:
                    cards_tensor[num][color][1] = 1
        return cards_tensor
    
    def tensor2cards(self):
        cards = []
        for num in range(15):
            for color in range(5):
                if self.tensor[num][color][0] == 1:
                    cards.append(card.Card(self.colorNum2Text_dict[color], num + 1))
                elif self.tensor[num][color][1] == 1:
                    cards.append(card.Card(self.colorNum2Text_dict[color], num + 1))
        if any(self.tensor[:,5,0]):
            cards.append(card.Card('Joker', None))
        if any(self.tensor[:,5,1]):
            cards.append(card.Card('Joker', None))
        return cards

    def tensor2cards_indices(self):
        cards = self.tensor2cards()
        cards_idx = []
        for c in cards:
            if (c.colour, c.number, 0) in self.cards_idx_dict:
                cards_idx.append(self.cards_idx_dict[(c.colour, c.number, 0)])
            if (c.colour, c.number, 1) in self.cards_idx_dict:
                cards_idx.append(self.cards_idx_dict[(c.colour, c.number, 1)])
        return cards_idx
    

    def __repr__(self):
        return repr(self.tensor.T)

    
    @classmethod
    # @staticmethod
    def random_cards_tensor(cls, num_cards=14):
        cards = []
        d = deck.Deck()
        for _ in range(num_cards):
            cards.append(d.deck.pop())
        return cls(cards)
        # return CardsTensor(np.random.randint(0, 2, (15, 6, 2)).__and__(CardsTensor(np.random.randint(0, 2, (15, 6, 2)))))
    
    
    def find_all_groups_tensor(self, card_tensor=None):
        card_tensor = self.tensor.copy() if card_tensor is None else card_tensor.copy()
        all_groups = []
        for number in range(self.number_num):
            # check if each color is available
            colors_available = [color for color in range(self.colour_num) if np.any(card_tensor[number, color, :])]
            
            if len(colors_available) >= 3:
                for i in range(3, len(colors_available) + 1):
                    for group_colors_tuple in itertools.combinations(colors_available, i):
                        group_tensor = self.create_group_tensor(number, group_colors_tuple, card_tensor)
                        all_groups.append(group_tensor)

        return all_groups

    def create_group_tensor(self, number, group_colors, card_tensor):
        group_tensor = np.zeros_like(card_tensor)
        for color in group_colors:
            # choose one card for each color（choose first deck first）
            deck = 0 if card_tensor[number, color, 0] > 0 else 1
            group_tensor[number, color, deck] = 1
        return CardsTensor(group_tensor)
    
    
    def find_all_runs_tensor(self, card_tensor=None):
        card_tensor = self.tensor.copy() if card_tensor is None else card_tensor.copy()
        all_runs = []

        for color in range(5):
            for start in range(11):  
                for end in range(start + 4, 15, 2):  # at least 3 cards in a run
                    if self.is_valid_run(card_tensor, start, end, color):
                        run_tensor = self.create_run_tensor(start, end, color, card_tensor)
                        all_runs.append(run_tensor)
                    else:
                        break  # no need to check longer runs
        return all_runs
    
    def is_valid_run(self, card_tensor, start, end, color):
        # successive odd or even numbers
        for number in range(start, end + 1, 2):  
            if not np.any(card_tensor[number, color, :]):
                return False
        return True

    def create_run_tensor(self, start, end, color, card_tensor):
        run_tensor = np.zeros_like(card_tensor)
        for number in range(start, end + 1, 2):  
            deck = 0 if card_tensor[number, color, 0] > 0 else 1
            run_tensor[number, color, deck] = 1
        return CardsTensor(run_tensor)

    # find all possible plays
    def find_all_plays(self, cards_tensor=None):
        all_plays = []

        all_plays.extend(self.find_all_groups_tensor(cards_tensor))
        all_plays.extend(self.find_all_runs_tensor(cards_tensor))

        # all_plays.append(["draw",])

        return all_plays
    
    def find_longest_combos(self, cards_tensor=None, current_play=[], best_play=None):
        cards_tensor = self.tensor.copy() if cards_tensor is None else cards_tensor
        best_play = ([], 0) if best_play is None else best_play

        # calculate the most-card combinations of cards
        current_play_cards_num = sum(play.sum() for play in current_play)

        if current_play_cards_num > best_play[1]:
            best_play = (current_play[:], current_play_cards_num)

        all_plays = self.find_all_plays(cards_tensor)
        for play in all_plays:
            new_cards_tensor = cards_tensor - play
            if np.all(new_cards_tensor >= 0):  # make sure no negative number in tensor
                best_play = self.find_longest_combos(new_cards_tensor, current_play + [play], best_play)

        return best_play
    
    
    def find_longest_combos_idx(self):
        longest_play, longest_num = self.find_longest_combos()
        return [self.from_tensor_to_indices(play) for play in longest_play], longest_num
    
    
    def find_max_sum_combos(self, cards_tensor=None, current_play=[], best_play=None):
        cards_tensor = self.tensor.copy() if cards_tensor is None else cards_tensor
        best_play = ([], 0) if best_play is None else best_play

        # calculate the biggest-sum-number combinations of cards
        current_play_number_num = sum([crd.number for play in current_play for crd in play.tensor2cards()])
                                # sum([crd.number for combo in best_play[0] for crd in combo.tensor2cards()])

        if current_play_number_num > best_play[1]:
            best_play = (current_play[:], current_play_number_num)

        all_plays = self.find_all_plays(cards_tensor)
        for play in all_plays:
            new_cards_tensor = cards_tensor - play
            if np.all(new_cards_tensor >= 0):  # make sure no negative number in tensor
                best_play = self.find_max_sum_combos(new_cards_tensor, current_play + [play], best_play)

        return best_play
    
    
    def find_max_sum_combos_idx(self):
        max_play, max_num = self.find_max_sum_combos()
        return [self.from_tensor_to_indices(play) for play in max_play], max_num
    
    
    def from_tensor_to_indices(self, cards_tensor):
        cards = cards_tensor.tensor2cards()
        cards_idx = []
        for c in cards:
            if (c.colour, c.number, 0) in self.cards_idx_dict:
                cards_idx.append(self.cards_idx_dict[(c.colour, c.number, 0)])
            if (c.colour, c.number, 1) in self.cards_idx_dict:
                cards_idx.append(self.cards_idx_dict[(c.colour, c.number, 1)])
        return cards_idx
    
    
    def add_cards_to_grid(self, cards_tensor, grid):
        # for card in cards_tensor.tensor2cards():
        #     
        # return grid
        pass
    
    
    def __getattr__(self, attr):
        # delegete all undefined method to ndarray
        return getattr(self.tensor, attr)
