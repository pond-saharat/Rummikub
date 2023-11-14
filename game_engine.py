class GameEngine:
    def __init__(self) -> None:
        self.deck = Deck()
        self.board = Board()
        
    def is_group(self, cards):
        if len(cards) < 3:
            return False
        
        regular_cards = [card for card in cards if card.number != 30]     
         
        if len(set([card.number for card in regular_cards])) != 1:
            return False
        else:
            return len(set([card.colour for card in regular_cards])) == len(regular_cards)
        
    def is_run(self, cards):
        if len(cards) < 3:
            return False

        regular_cards = [card for card in cards if card.number != 30] 
        wild_cards_count = len([card for card in cards if card.number == 30]) 

        if len(set([card.colour for card in regular_cards])) != 1:
            return False
        else:
            cards_number = [card.number for card in regular_cards]
            cards_number.sort()
            for i in range(1, len(cards_number)):
                if cards_number[i] != cards_number[i-1] + 1:
                    if wild_cards_count == 0:
                        return False
                    wild_cards_count -= 1
            return True 
    
    def is_valid(self, cards):
        return self.is_group(cards) or self.is_run(cards)              
    
    def is_first_move_valid(self, cards):
        if self.is_valid(cards):                
            total_points = sum(card.number for card in cards)
            if total_points >= 30:
                return True
        else:
            return False
        
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
                    
                    # if self.find_combinations(cards_left):
                    #     combinations.append(cards_left)
        return combinations        
    
    
    def check_combinations(self, tiles):
        tiles.sort(key=lambda tile: (tile.number, tile.colour))
        print(tiles)
        for i in range(1, len(tiles) + 1):
            first_group = tiles[:i]
            if self.is_valid(first_group):
                remaining_tiles = tiles[i:]
                if not remaining_tiles or self.check_combinations(remaining_tiles):
                    return 1 + (self.check_combinations(remaining_tiles) if remaining_tiles else 0)
        return 0
    
    
    def check_all_combinations(self, tiles, combination=[], remaining=None):
        if remaining is None:
            remaining = tiles.copy()

        if not remaining:
            return all(self.is_valid(group) for group in combination)

        for i in range(len(remaining)):
            next_tile = remaining.pop(0)
            for group in combination:
                group.append(next_tile)
                if self.check_all_combinations(tiles, combination, remaining):
                    return True
                group.pop()

            combination.append([next_tile])
            if self.check_all_combinations(tiles, combination, remaining):
                return True
            combination.pop()
            remaining.append(next_tile)
        return False
    
    
    
    def find_all_combinations(self, tiles):
        valid_combinations = set()
        self._find_combinations_recursive(tiles, [], tiles.copy(), valid_combinations)
        
        return [list(map(self._convert_to_tile, comb)) for comb in valid_combinations]

    def _convert_from_hashable(self, hashable_combination):
        return [[Card(color, int(number)) for number, color in (tile_str.split() for tile_str in group)] for group in hashable_combination]

    def _convert_to_tile(self, group):
        return [Card(color, int(number)) for number, color in (tile_str.split() for tile_str in group)]
    
    def _convert_combination_to_hashable(self, combination):
        return tuple(tuple(f"{tile.number} {tile.colour}" for tile in sorted(group, key=lambda t: (t.number, t.colour))) for group in combination)

    def _find_combinations_recursive(self, tiles, current_combination, remaining, valid_combinations):
        if not remaining:
            if all(self.is_valid(group) for group in current_combination):
                valid_combinations.add(self._convert_combination_to_hashable(current_combination))
            return

        for i in range(len(remaining)):
            next_tile = remaining.pop(0)
            for group in current_combination:
                group.append(next_tile)
                self._find_combinations_recursive(tiles, current_combination, remaining, valid_combinations)
                group.pop()

            new_combination = current_combination + [[next_tile]]
            self._find_combinations_recursive(tiles, new_combination, remaining, valid_combinations)

            remaining.append(next_tile)
            
    def first_move(self, player, card_sets):
        if all(card in player.hands for card_set in card_sets for card in card_set):
            if all(self.is_first_move_valid(card_set) for card_set in card_sets):
                player.hands = [card for card in player.hands if card not in card_set for card_set in card_sets]
                self.board.add_all_card_sets(card_sets)
                print('move success')
            else: 
                print("move failed")
        else:
            print("move failed")
            
            
    # card sets, corresponding nums in board
    def regular_move(self, player, card_sets, sets_nums_in_board):
        if all(card in player.hands for card_set in card_sets for card in card_set) and len(card_sets) == len(sets_nums_in_board):
            if all(self.is_valid(self.board.board[i].extend(card_sets[i])) for i in range(len(card_sets))):
                for i in range(len(card_sets)):
                    self.board.add_card_set_with_num(card_sets[i], sets_nums_in_board[i])
                