import pygame
import game_engine
import menu
import board
import cardset
import card as c
import button
import player
import timer as t
from pygame.locals import *
from config import *
import bot
import time


class GameUI:
    def __init__(self,num_of_game=0,num_of_ais=0,num_of_humans = 4):
        self.running = True
        # Initialize an empty group of game objects
        self.sprites = pygame.sprite.Group()

        pygame.init()
        # Create a blank screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.screen.fill(BACKGROUND_COLOUR)
        pygame.mouse.set_visible(1)
        pygame.display.set_caption(CAPTION)
        # Refer ui engine location to ui game location and refer game engine location to ui engine location
        self.game_state = "main_menu"
        self.pause_state= False
        self.num_of_ais = num_of_ais
        self.num_of_humans = num_of_humans
        if self.game_state == "main_menu" and num_of_game == 0:
            menu.Menu(self).run()
        elif num_of_game != 0:
            self.game_state = "game"
        print("Number of AI players: ", self.num_of_ais)
        print("Number of human players: ", self.num_of_humans)
        self.game_engine = game_engine.GameEngine(self)
        self.game_engine.screen = self.screen

        # button settings
        self.ui_objects = []
        self.ui_objects.append(button.EndTurnButton(END_TURN_BUTTON_REGION,"End turn",36))
        self.play_for_me_button = button.PlayForMeButton(PLAY_FOR_ME_BUTTON_REGION,"Play for me",36)
        self.ui_objects.append(button.FlipAllCardsButton(FLIP_ALL_CARDS_BUTTON_REGION,"Flip all cards",36))
        self.ui_objects.append(button.HintButton(HINT_BUTTON_REGION,"Give me a hint",36))
        self.draw_button = button.DrawButton(DRAW_BUTTON_REGION,"Draw",36)
        self.ui_objects.append(self.play_for_me_button)
        self.ui_objects.append(self.draw_button)
        self.draw_region = None
        self.game_engine.update_objects()

        # text settings
        self.notification = "Welcome to Rummikub!"
        # drag and drop settings
        self.dragging = False
        self.card_being_dragged = None
        self.offset_x = 0
        self.offset_y = 0
        self.grid_cards = board.Board().grid_cards # { (row, col): [card1, card2, ...], ... }
        self.selected_cards = self.game_engine.current_player.selected_cards

    # Run the game loop
    def run(self):
        # Add all sprites
        self.add_all_sprites()

        # deal cards
        # self.game_engine.deal_cards()
        self.set_current_player_hands()
        self.timer = t.Timer(max_time = MAX_TIME+10)
        # Infinite loop
        while self.running:
            # Check the game state   
            if self.game_state == "Rummikub!":
                menu.Menu(self).run(finish=True)
                return {self.game_engine.winning_score:list(map(str,self.game_engine.winners))}, self.num_of_ais, self.num_of_humans
            elif self.game_state == "game":
                # Fill backgroud colour
                self.screen.fill(BACKGROUND_COLOUR)
                self.game_engine.draw_regions()
                
                
                # Draw background elements
                self.draw_grid(self.screen)
                self.pause_state=True
                # Display text
                notification_surface = pygame.font.SysFont(None, 24).render(self.notification, True, (255, 255, 255)) 
                
                turn_surface = pygame.font.SysFont(None, 26).render(f"Turn: {self.game_engine.current_player}", True, (255, 255, 255)) 
                score_surface = pygame.font.SysFont(None, 26).render(f"Score: {self.game_engine.current_player.score}", True, (255, 255, 255)) 
                self.screen.blit(turn_surface, NOTIFICATION_REGION_1)
                self.screen.blit(score_surface, NOTIFICATION_REGION_2)
                self.screen.blit(notification_surface, NOTIFICATION_REGION_3)

                if isinstance(self.game_engine.current_player, player.HumanPlayer):
                
                    # Check the inputs provided by the user
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            # if event.key == pygame.K_SPACE: 
                            if event.key == pygame.K_ESCAPE: 
                                menu.Menu(self).run(game_paused=True)
                            
                        self.check_event(event,self.game_engine)
                elif isinstance(self.game_engine.current_player, player.AIPlayer):
                    self.play_for_me_button.left_click_up_action(self)
                    # pygame.time.delay(DELAY_TIME)
                    
                else:
                    pass
                # draw grid
                
                # self.draw_hands_region()

                # draw button
                # pygame.draw.rect(self.screen, (200, 200, 200), self.button_rect)
                # self.screen.blit(
                #     self.button_text, (self.button_rect.x + 20, self.button_rect.y + 10)
                # )
                # Draw all of the sprites
                # self.set_current_player_hands()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for sprite in self.sprites:
                    if sprite.rect.collidepoint(mouse_x,mouse_y) and isinstance(sprite,c.Card):
                        if sprite.visible and (sprite.owner == self.game_engine.current_player or sprite.owner is None):
                            offset = 10
                            highlight = pygame.Surface((sprite.rect.width+offset, sprite.rect.height+offset), pygame.SRCALPHA)
                            highlight_rect = highlight.get_rect()
                            highlight_rect.center = sprite.rect.center
                            if isinstance(sprite,c.ColourCard):
                                pygame.draw.rect(self.screen,sprite.colour,highlight_rect, border_radius=0)
                            elif isinstance(sprite,c.JokerCard):
                                pygame.draw.rect(self.screen,"black",highlight_rect, border_radius=0)
                    elif sprite.rect.collidepoint(mouse_x,mouse_y):
                        offset = 15
                        highlight = pygame.Surface((sprite.rect.width+offset, sprite.rect.height+offset), pygame.SRCALPHA)
                        highlight_rect = highlight.get_rect()
                        highlight_rect.center = sprite.rect.center
                        pygame.draw.rect(self.screen,(255, 255, 150, 0),highlight_rect, border_radius=0)
                    else:
                        pass
                    
                    sprite.draw(self.screen)
                    
                    
                    

                # Highlight selected cards
                for card in self.selected_cards:
                    if isinstance(card, c.ColourCard):
                        pygame.draw.rect(self.screen, card.colour, card.rect, 3)
                    elif isinstance(card, c.JokerCard):
                        pygame.draw.rect(self.screen, "black", card.rect, 3)
                    else:
                        pass
                self.timer.display(self)
                pygame.display.flip()
            else:
                pass

    
    def add_all_sprites(self):
        for obj in self.game_engine.objects:
            self.sprites.add(obj)

    # Check input events by the user
    def check_event(self, event, game_engine):
        
        # Quit the game if the event is QUIT
        if event.type == pygame.QUIT:
            self.running = False
            return
        # Check for mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = event.pos
            if event.button == 1:
                for sprite in self.sprites:
                    # Check if the mouse click is within sprites' boundaries
                    if sprite.rect.collidepoint(mouse_x, mouse_y):
                        if isinstance(sprite, c.Card):
                            if sprite.owner == self.game_engine.current_player or sprite.owner is None:
                                self.start_dragging(sprite, event.pos)
                                break
                        elif isinstance(sprite, button.GameButton):
                            sprite.left_click_action(self)
                            break
                        else:
                            pass
            elif event.button == 3:
                self.selected_cards = []
            else:
                pass

        # handle dropping card
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if event.button == 1 and self.dragging:  # left button released
                self.dragging = False
                mouse_x, mouse_y = event.pos
                for sprite in self.sprites:
                    # other_sprites = [s for s in self.sprites if s != sprite]
                    if isinstance(sprite,c.Card):
                        if (sprite.rect.collidepoint(event.pos) ):
                            # if the card is in the selected_cards, remove it from the selected_cards
                            if sprite in self.selected_cards:
                                self.selected_cards.remove(sprite)
                            else:
                                if len([c for c in self.selected_cards if c in self.draw_button.cards]) > 0 and sprite in self.draw_button.cards:
                                    self.notification = "You must choose only one"
                                    self.selected_cards = []
                                
                                if len(self.selected_cards) < 8 and (sprite.owner == self.game_engine.current_player or sprite.owner is None):
                                    self.selected_cards.append(sprite)
                                elif sprite.owner != self.game_engine.current_player:
                                    # self.notification = "You can only select your own cards"
                                    self.selected_cards = []
                                elif len(self.selected_cards) >= 8:
                                    self.selected_cards.pop(0)
                                    self.selected_cards.append(sprite)
                                else:
                                    self.selected_cards.append(sprite)
                    else:
                        pass
                self.drop_card(game_engine)
            elif event.button == 1:
                for sprite in self.sprites:
                    if isinstance(sprite, c.Card):
                        pass
                    elif isinstance(sprite, button.GameButton):
                        if sprite.rect.collidepoint(mouse_x, mouse_y):
                            sprite.left_click_up_action(self)
                        sprite.clicked = False
                    else:
                        pass
            else:
                pass
        
        # handle dragging
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            if self.card_being_dragged is not None:
                mouse_x, mouse_y = event.pos
                for card in self.cards_being_dragged:
                    new_x = mouse_x + self.offset_x
                    new_y = mouse_y + self.offset_y

                    # update the card's position
                    new_x = max(0, min(SCREEN_WIDTH - card.rect.width, new_x))
                    new_y = max(0, min(SCREEN_HEIGHT - card.rect.height, new_y))
                    card.rect.x = new_x
                    card.rect.y = new_y
                # draw the dragged card
                # self.card_being_dragged.draw(self.game_engine)
        else:
            pass

    # Draw lines of the grid
    def draw_grid(self, screen):
        grid_colour = (16, 38, 59, 0.1)
        # grid_colour = (215, 51, 108)
        for x in range(WIDTH_2_COLUMNS, WIDTH_2_COLUMNS + BOARD_WIDTH + 1, GRID_WIDTH):
            pygame.draw.line(
                screen, grid_colour, (x, HEIGHT_1_ROW), (x, HEIGHT_1_ROW + BOARD_HEIGHT)
            )
        for y in range(HEIGHT_1_ROW, HEIGHT_1_ROW + BOARD_HEIGHT + 1, GRID_HEIGHT):
            pygame.draw.line(
                screen, grid_colour, (WIDTH_2_COLUMNS, y), (WIDTH_2_COLUMNS + BOARD_WIDTH, y)
            )

    def find_nearest_grid_pos(self, x, y):
        x_board = x - WIDTH_2_COLUMNS
        y_board = y - HEIGHT_1_ROW

        grid_x = x_board // GRID_WIDTH * GRID_WIDTH + CARD_WIDTH // 2 + WIDTH_2_COLUMNS
        grid_y = y_board // GRID_HEIGHT * GRID_HEIGHT + GRID_HEIGHT // 2 + HEIGHT_1_ROW
        return grid_x, grid_y

    def find_nearest_grid(self, x, y):
        x_board = x - WIDTH_2_COLUMNS
        y_board = y - HEIGHT_1_ROW

        col = x_board // GRID_WIDTH
        row = y_board // GRID_HEIGHT
        return row, col

    def sort_grid(self, grid_cards):
        # if (row, col) in grid_cards
        for _ in grid_cards.keys():
            if not cardset.CardSet.is_valid(grid_cards[_]):
                grid_cards[_] = list(set(grid_cards[_]))
                grid_cards[_].sort(key=lambda crd: (crd.colour, crd.number))
                for i, card in enumerate(grid_cards[_]):
                    card_grid_x, card_grid_y = self.find_nearest_grid_pos(
                        card.rect.centerx, card.rect.centery
                    )
                    card.rect.centerx = card_grid_x + CARD_WIDTH * i + GAP * i + GAP 
                    card.rect.centery = card_grid_y
            else:
                grid_cards[_] = cardset.CardSet.sort_list(grid_cards[_])
                for i, card in enumerate(grid_cards[_]):
                    card_grid_x, card_grid_y = self.find_nearest_grid_pos(
                        card.rect.centerx, card.rect.centery
                    )
                    card.rect.centerx = card_grid_x + CARD_WIDTH * i + GAP * i + GAP
                    card.rect.centery = card_grid_y

    def set_current_player_hands(self):
        for p, player in enumerate(self.game_engine.players):
            player.hands.sort(key=lambda crd: (crd.colour, crd.number))
            if p == 0:
                for i, card in enumerate(player.hands):
                    card.rect.centerx = WIDTH_2_COLUMNS + CARD_WIDTH // 2 + CARD_WIDTH * i + GAP * i + GAP 
                    card.rect.centery = HEIGHT_1_ROW + CARD_HEIGHT // 2 + BOARD_HEIGHT + GAP
            elif p == 1:
                i, j = 0, 0
                for card in player.hands:
                    card.rect.centerx = CARD_WIDTH // 2 + CARD_WIDTH * i + GAP * i + GAP 
                    card.rect.centery = HEIGHT_1_ROW + CARD_HEIGHT // 2 + CARD_HEIGHT * j + GAP * j + GAP
                    i += 1
                    if i == 2:
                        i = 0
                        j +=1
            elif p == 2:
                for i, card in enumerate(player.hands):
                    card.rect.centerx = WIDTH_2_COLUMNS + CARD_WIDTH // 2 + CARD_WIDTH * i + GAP * i + GAP 
                    card.rect.centery = CARD_HEIGHT // 2 + GAP
            elif p == 3:
                i, j = 0, 0
                for card in player.hands:
                    card.rect.centerx = BOARD_WIDTH + WIDTH_2_COLUMNS + CARD_WIDTH // 2 + CARD_WIDTH * i + GAP * i + GAP 
                    card.rect.centery = HEIGHT_1_ROW + CARD_HEIGHT // 2 + CARD_HEIGHT * j + GAP * j + GAP
                    i += 1
                    if i == 2:
                        i = 0
                        j +=1
            else:
                pass
            
    
    def find_hands_destination(self, card_list, player):
        dest_xy = []

        if int(player.name[-1]) == 0:
            offset_x = WIDTH_2_COLUMNS + GAP + (CARD_WIDTH + GAP) * len(player.hands) + CARD_WIDTH // 2 
            offset_y = HEIGHT_1_ROW + BOARD_HEIGHT + GAP + CARD_HEIGHT // 2
            for i in range(len(card_list)):                
                card_x = offset_x + CARD_WIDTH * i + GAP * i
                dest_xy.append((card_x, offset_y))
            return dest_xy
            
        elif int(player.name[-1]) == 1:
            offset_x = GAP + CARD_WIDTH // 2 + (len(player.hands) % 2) * (GAP) 
            offset_y = HEIGHT_1_ROW + CARD_HEIGHT // 2 + (CARD_HEIGHT + GAP) * (len(player.hands) // 2)
            i, j = len(player.hands) % 2, 0 
            for _ in range(len(card_list)):                
                card_x = offset_x + CARD_WIDTH * i + GAP * i
                card_y = offset_y + CARD_HEIGHT * j + GAP * j
                dest_xy.append((card_x, card_y))
                i += 1
                if i == 2:
                    i = 0
                    j +=1
            return dest_xy
            
        elif int(player.name[-1]) == 2:
            offset_x = WIDTH_2_COLUMNS + GAP + (CARD_WIDTH + GAP) * len(player.hands) + CARD_WIDTH // 2 
            offset_y = CARD_HEIGHT // 2 + GAP
            for i in range(len(card_list)):                
                card_x = offset_x + CARD_WIDTH * i + GAP * i
                dest_xy.append((card_x, offset_y))
            return dest_xy
            
        elif int(player.name[-1]) == 3:
            offset_x = BOARD_WIDTH + WIDTH_2_COLUMNS + GAP + CARD_WIDTH // 2 + (len(player.hands) % 2) * ( GAP) 
            offset_y = HEIGHT_1_ROW + CARD_HEIGHT // 2 + (CARD_HEIGHT + GAP) * (len(player.hands) // 2)
            i, j = len(player.hands) % 2, 0 
            for _ in range(len(card_list)):                
                card_x = offset_x + CARD_WIDTH * i + GAP * i
                card_y = offset_y + CARD_HEIGHT * j + GAP * j
                dest_xy.append((card_x, card_y))
                i += 1
                if i == 2:
                    i = 0
                    j +=1
            return dest_xy
            
        else:
            pass

    def start_dragging(self, card, mouse_pos):
        self.dragging = True
        self.card_being_dragged = card
        self.offset_x = card.rect.x - mouse_pos[0]
        self.offset_y = card.rect.y - mouse_pos[1]

        # if the card in selected_cards, drag all the selected cards
        if card in self.selected_cards:
            self.cards_being_dragged = list(self.selected_cards)
        else:
            self.cards_being_dragged = [card]

        # record the original position of the cards
        self.original_positions = {}
        self.original_xy = {}
        for selected_card in self.cards_being_dragged:
            grid_pos = self.find_nearest_grid(
                selected_card.rect.centerx, selected_card.rect.centery
            )
            self.original_positions[selected_card] = grid_pos
            self.original_xy[selected_card] = (
                selected_card.rect.centerx,
                selected_card.rect.centery,
            )

    def drop_card(self, game_engine):
        # self.dragging = False
        dropped_pos_x, dropped_pos_y = self.card_being_dragged.rect.centerx, self.card_being_dragged.rect.centery

        # If the current drop position is in current player's hand region -> leave a card in that region
        if game_engine.current_player.hand_region.collidepoint(dropped_pos_x, dropped_pos_y):
            for card in self.cards_being_dragged:
                if card not in game_engine.current_player.hands: #  and card not in self.draw_button.cards:
                    game_engine.current_player.hands.append(card)
                
                if card in game_engine.deck.deck and card in self.draw_button.cards:
                    self.draw_button.cards.remove(card)
                    game_engine.deck.deck.remove(card)
                    self.draw_button.reset()
                    # if all(cardset.CardSet.is_valid(grid_cell) for grid_cell in self.grid_cards.values()):
                    self.game_engine.current_player.made_move = True
                    
                card.owner = game_engine.current_player
                
            for key, card_list in self.grid_cards.items():
                self.grid_cards[key] = [crd for crd in card_list if crd not in self.cards_being_dragged]
            print("selected cards:", self.selected_cards)
            print("grid:", self.grid_cards)
            print("hands:", game_engine.current_player.hands)
            self.reset_drag_parameters()
            self.set_current_player_hands()
            return
        
        # find the nearest grid to the card
        row, col = self.find_nearest_grid(dropped_pos_x, dropped_pos_y)

        # add the new grid to the grid_cards if it is not in the grid_cards
        if (row, col) not in self.grid_cards.keys():
            self.grid_cards[(row, col)] = []

        for card in self.cards_being_dragged:
            original_grid = self.original_positions[card]
            original_xy = self.original_xy[card]
            # if (row, col) == original_grid:
            #     card.rect.centerx = original_xy[0]
            #     card.rect.centery = original_xy[1]
            #     self.grid_cards[(row, col)].append(card)

            ## if this is a valid position, put the card to the grid
            if self.is_valid_grid_position(row, col):
                if cardset.CardSet.is_valid(self.grid_cards[(row, col)] + [card]):
                    self.game_engine.current_player.made_move = True
                else:
                    self.game_engine.current_player.made_move = False
                
                # if the grid is full, put the card back to the original position
                if self.is_grid_full(row, col):
                    card.rect.centerx = original_xy[0]
                    card.rect.centery = original_xy[1]
                    continue
                
                if card in game_engine.deck.deck and card in self.draw_button.cards:
                    self.draw_button.cards.remove(card)
                    game_engine.deck.deck.remove(card)
                    self.draw_button.reset()
                    self.game_engine.current_player.made_move = True

                # remove the card from the original grid
                if (original_grid in self.grid_cards and card in self.grid_cards[original_grid]):
                    self.grid_cards[original_grid].remove(card)
                    
                # if the card is in the selected_cards, put all the selected cards to the grid
                self.place_card_to_grid(card, row, col, self.card_being_dragged)

                # Reset the owner of the card
                if card.owner:
                    card.owner.hands.remove(card)
                    card.owner = None

                card.owner = None

            ## if the card is outside the board, put it back to the original position
            else:
                card.rect.centerx = original_xy[0]
                card.rect.centery = original_xy[1]
                self.selected_cards = []

        # Reset dragging parameters to their initial values
        self.reset_drag_parameters()
        self.set_current_player_hands()

        # if all(card in self.grid_cards[(row, col)] for card in self.selected_cards):
        #     self.selected_cards = []
        # remove empty keys and sort the cards in each grid
        self.grid_cards = {k: v for k, v in self.grid_cards.items() if v != []}
        self.sort_grid(self.grid_cards)
        
        print("selected cards:", self.selected_cards)
        print("grid:", self.grid_cards)
        pygame.display.flip()

    def reset_drag_parameters(self):
        self.game_engine.current_player.selected_cards = []
        for card in self.game_engine.current_player.hands:
            card.is_selected = False
        for _, cards in self.grid_cards.items():
            for card in cards:
                card.is_selected = False
        self.game_engine.selected_cards = []
        self.card_being_dragged = None
        self.cards_being_dragged = []
        self.original_positions = {}
        self.original_xy = {}
    
    def is_valid_grid_position(self, row, col):
        return (
            0 <= row < BOARD_HEIGHT // GRID_HEIGHT 
            and 0 <= col < BOARD_WIDTH // GRID_WIDTH 
        )


    def place_card_to_grid(self, card, row, col, card_being_dragged):
        grid_x, grid_y = self.find_nearest_grid_pos(
            card_being_dragged.rect.centerx, card_being_dragged.rect.centery
        )
        
        card.rect.centerx = (
            grid_x
            + CARD_WIDTH * len(self.grid_cards[(row, col)])
            + GAP * len(self.grid_cards[(row, col)])
            + GAP
        )
        card.rect.centery = grid_y

        # if card not in self.grid_cards[(row, col)]:
        self.grid_cards[(row, col)].append(card)
        # self.selected_cards = []

    def show_players_hands(self):
        for player in self.game_engine.players:
            print(player.name, player.hands)

    def is_grid_full(self, row, col):
        return len(self.grid_cards[(row, col)]) >= 8
    
    def find_empty_grid(self):
        empty_grid = []
        for row in range(8):
            for col in range(2):
                if (row, col) not in self.grid_cards.keys():
                    empty_grid.append((row, col))
        return empty_grid
    
    def play_for_me(self):
        empty_grid = self.find_empty_grid()
        if empty_grid == []:
            self.notification = "No empty grid"
            '''draw a card'''
            self.game_engine.current_player.draw_one_card(game_ui=self)
            # self.notification = "No combos"
            self.game_engine.next_turn()
            return
        
        if self.game_engine.current_player.first_moved == False:            
            self.play_cards_from_hand()
        else:
            # self.play_cards_from_hand()
            # self.manipulate_hands_and_grid_cards()
            self.play_cards_from_hand()
            # self.add_hands_cards_to_grid()
        
    
    def play_cards_from_hand(self):
        
        empty_grid = self.find_empty_grid()
        if empty_grid == []:
            self.notification = "No empty grid"
            '''draw a card'''
            self.game_engine.current_player.draw_one_card(game_ui=self)
            # self.notification = "No combos"
            self.game_engine.next_turn()
            return
        
        # Find the best combos of hand card indices
        hand_cards_tensor = bot.CardsTensor(cards=self.game_engine.current_player.hands)
        best_play_idx_combos, sum = hand_cards_tensor.find_max_sum_combos_idx()
        all_indices = [i for combo in best_play_idx_combos for i in combo]
        cards_in_best_play = [
            self.game_engine.current_player.hands[i] for i in all_indices
        ]
        
        if len(best_play_idx_combos) > len(empty_grid):
            best_play_idx_combos = best_play_idx_combos[:len(empty_grid)]
        
        # no combos found in hand
        if best_play_idx_combos == []:
            '''draw a card'''
            self.game_engine.current_player.draw_one_card(game_ui=self)
            # self.notification = "No combos"
            self.game_engine.next_turn()
            self.notification = "Drew a card"
            # time.sleep(3)
        
        # first move
        elif self.game_engine.current_player.first_moved == False:
            self.place_combos_to_empty_grid(best_play_idx_combos, empty_grid)
            
            self.notification = f"First moved {cards_in_best_play}"
            self.game_engine.current_player.first_moved = True
            self.game_engine.current_player.made_move = True
            self.game_engine.next_turn()
        
        # not first move, regular move
        else:
            self.place_combos_to_empty_grid(best_play_idx_combos, empty_grid)
            self.grid_cards = {k: v for k, v in self.grid_cards.items() if v != []}
            self.notification = f"Made a move {cards_in_best_play}"
            
            self.sort_grid(self.grid_cards)
            self.add_hands_cards_to_grid()
            
            self.game_engine.current_player.made_move = True
            self.game_engine.next_turn()
    
    
    
    def add_hands_cards_to_grid(self):
        hand_cards = self.game_engine.current_player.hands
        
        for pos, cell_cards in self.grid_cards.items():
            all_combos = self.find_combos_to_group_cell(hand_cards, cell_cards)
            
            # longest_combo = max(all_combos, key=lambda combo: sum([card.number for card in combo if card.number is not None]))
            if all_combos == [[]] or all_combos == [] or c.JokerCard() in all_combos[0]:
                continue
            print("all_combos:", all_combos)
            longest_combo = max(all_combos, key=len)
            
            # # longest_combo = all_combos[0]
            # longest_combo_tensor = bot.CardsTensor(cards=longest_combo)
            # cards_idx = longest_combo_tensor.from_tensor_to_indices(longest_combo_tensor)

            # self.place_combos_to_empty_grid(cards_idx, pos)
            self.place_combos_to_add_grids([longest_combo], [pos])
            
            # self.place_combos_to_add_grids(all_combos, [pos for _ in range(len(all_combos))])
    
    
    
    def manipulate_hands_and_grid_cards(self):
        # self.grid_cards_tensor = {pos: bot.CardsTensor(cards=cards) for pos, cards in self.grid_cards.items()}
        
        # for pos, cards_tensor in self.grid_cards_tensor.items():
        #     if cardset.CardSet.is_valid(grid_cards[_]):
            
        # for pos, cards in self.grid_cards.items():
            # if cardset.CardSet.is_group(cards):
                # self.find_cards_to_add_to_group(pos, cards) -> index of cards in hand to add to group
        
        
        
        test = self.find_max_sum_play_to_add()
        print(test)
        
        
        
        
        pass
    
    
    def find_max_sum_play_to_add(self, cards_list=None, grid_cards=None, current_play=[], best_play=None):
        cards_list = self.game_engine.current_player.hands.copy() if cards_list is None else cards_list
        grid_cards = self.grid_cards.copy() if grid_cards is None else grid_cards
        best_play= ([], 0) if best_play is None else best_play
        
        # calculate the sum of the cards to add to grid
        # current_play_sum = sum([card.number for card in current_play])
        current_play_sum = sum([card.number for play_and_pos in current_play for card in play_and_pos[0] if card.number is not None])
        
        if current_play_sum > best_play[-1]:
            best_play = (current_play[:], current_play_sum)
        
        # plays_and_pos: [(play, pos) for all plays->list to add and their positions->tuple]
        all_plays_and_pos = self.find_all_plays_to_add(cards_list, grid_cards)
        for play_and_pos in all_plays_and_pos:
            play, pos = play_and_pos
            # print("play:", play)
            # print("pos:", pos)
            # print("current_play:", current_play)
            # print("best_play:", best_play)
            print("cards_list:", cards_list)
            new_cards_list = [card for card in cards_list if card not in play]
            
            new_current_play = current_play + [play_and_pos]
            new_grid_cards = {k: v for k, v in grid_cards.items() if k != pos}
            if len(new_cards_list) > 0:
                best_play = self.find_max_sum_play_to_add(new_cards_list, new_grid_cards, new_current_play, best_play)
        
        return best_play
        # pass
    
    
    # return the cards in hand to add to the group
    def find_all_plays_to_add(self, cards_list, grid_cards):
        all_plays = {pos: [] for pos in grid_cards.keys()}
        for pos, cell_cards in grid_cards.items():
            if cardset.CardSet.is_group(cell_cards):
                plays = self.find_combos_to_group_cell(cards_list, cell_cards)
                all_plays[pos].extend(plays)
            elif cardset.CardSet.is_run(cell_cards):
                plays = self.find_combos_to_run_cell(cards_list, cell_cards)
                all_plays[pos].extend(plays)
            else:
                pass
        plays_to_add = {pos: plays for pos, plays in all_plays.items() if plays != []}
        plays_and_pos = [(play, pos) for pos, plays in plays_to_add.items() for play in plays]
        return plays_and_pos
    
    
    def find_combos_to_group_cell(self, cards_list, cell_cards):
        all_combos = []
        if cardset.CardSet.is_group(cell_cards):
            cards4group = []
            
            for card in cards_list:
                if cardset.CardSet.is_group(cell_cards + [card]) and card.colour not in [c.colour for c in cards4group]:
                    cards4group.append(card)
            
            all_combos = [[_] for _ in cards4group] + list([cards4group])
        return all_combos
    
    def find_combos_to_run_cell(self, cards_list, cell_cards):
        all_combos = []
        if cardset.CardSet.is_run(cell_cards):
            
            cards4run = []
            for card in cards_list:
                if cardset.CardSet.is_run(cell_cards + [card]) and card.number not in [c.number for c in cards4run]:
                    cards4run.append(card)

                
            
            
        # now all_combos still []
        return all_combos 
            
            
    
    def can_add_cards_to_cell(self, cards_list, cell_cards):
        return cardset.CardSet.is_valid(cell_cards + cards_list)
    
    
    
    def place_combos_to_empty_grid(self, best_play_idx_combos, empty_grid):
        # empty_grid = self.find_empty_grid()
        # hand_cards_tensor = bot.CardsTensor(cards=self.game_engine.current_player.hands)
        # best_play_idx_combos, sum = hand_cards_tensor.find_max_sum_combos_idx()
        all_indices = [i for combo in best_play_idx_combos for i in combo]
        all_combos_cards = [self.game_engine.current_player.hands[i] for i in all_indices]
        combos_num = len(best_play_idx_combos)
        empty_grid_num = len(empty_grid)
        
        for i in range(min(combos_num, empty_grid_num)):
            combo = best_play_idx_combos[i]
            row, col = empty_grid[i]
            self.place_combo_to_grid(combo, row, col)
            
        
        self.game_engine.current_player.hands = [card for card in self.game_engine.current_player.hands if card not in all_combos_cards]
        self.reset_drag_parameters()
        self.set_current_player_hands()
        self.grid_cards = {k: v for k, v in self.grid_cards.items() if v != []}
        self.sort_grid(self.grid_cards)
        self.game_engine.current_player.made_move = True
        return True


    def place_cards_to_one_cell(self, cards, row, col):
        if (row, col) not in self.grid_cards.keys():
            self.grid_cards[(row, col)] = []
        # else:
        #     print(f"This grid {(row, col)} is not empty")
        #     return False
        
        grid_x = WIDTH_2_COLUMNS + col * GRID_WIDTH + CARD_WIDTH // 2 + GAP + CARD_WIDTH * len(self.grid_cards[(row, col)]) + GAP * len(self.grid_cards[(row, col)])
        grid_y = HEIGHT_1_ROW + row * GRID_HEIGHT + GRID_HEIGHT // 2 + GAP
        
        dest_xy = [(grid_x + CARD_WIDTH * i + GAP * i + GAP, grid_y) for i in range(len(cards))]
        
        # animation of dragging the cards to the grid
        self.move_cards_animation(cards, dest_xy)
        
        for card in cards:
            # card = self.game_engine.current_player.hands[idx]
            card.owner = None
            card.is_selected = False
            
            self.grid_cards[(row, col)].append(card)
            if card in self.game_engine.current_player.hands:
                self.game_engine.current_player.hands.remove(card)
        
        self.sort_grid(self.grid_cards)
        self.selected_cards = []

    
    def place_combo_to_grid(self, combo, row, col):
        if (row, col) not in self.grid_cards.keys():
            self.grid_cards[(row, col)] = []
        # else:
        #     print(f"This grid {(row, col)} is not empty")
        #     return False
        
        grid_x = WIDTH_2_COLUMNS + col * GRID_WIDTH + CARD_WIDTH // 2 + GAP + CARD_WIDTH * len(self.grid_cards[(row, col)]) + GAP * len(self.grid_cards[(row, col)])
        grid_y = HEIGHT_1_ROW + row * GRID_HEIGHT + GRID_HEIGHT // 2 + GAP
        
        print("combo:", combo)
        print("hands:", self.game_engine.current_player.hands)
        cards = [self.game_engine.current_player.hands[idx] for idx in combo]
        dest_xy = [(grid_x + CARD_WIDTH * i + GAP * i + GAP, grid_y) for i in range(len(cards))]
        
        # animation of dragging the cards to the grid
        self.move_cards_animation(cards, dest_xy)
        
        for card in cards:
            # card = self.game_engine.current_player.hands[idx]
            card.owner = None
            card.is_selected = False
            
            self.grid_cards[(row, col)].append(card)
            # self.game_engine.current_player.hands.remove(card)
        
        self.sort_grid(self.grid_cards)
        self.selected_cards = []
    
    # animate the cards to the grid
    def move_cards_animation(self, cards, dest_xy):
        origin_xy = [(card.rect.centerx, card.rect.centery) for card in cards]
        velocity = [((dest_xy[i][0] - origin_xy[i][0]) // 30, (dest_xy[i][1] - origin_xy[i][1]) //30) for i in range(len(cards))]
        
        # drag the cards to the grid
        for _ in range(30):
            # update the position of the cards
            for i, card in enumerate(cards):
                card.rect.centerx += velocity[i][0]
                card.rect.centery += velocity[i][1]
            # draw the dragged card
            self.screen.fill(BACKGROUND_COLOUR)
            self.game_engine.draw_regions()
            self.draw_grid(self.screen)
            self.timer.display(self)
            for sprite in self.sprites:
                sprite.draw(self.screen)
            pygame.display.flip()
            pygame.time.wait(10)
        
        return True
    
    
    def place_combos_to_add_grids(self, cards_combos, grids):
        
        # all_indices = [i for combo in best_play_idx_combos for i in combo]
        all_combos_cards = [crd for combo in cards_combos for crd in combo]
        combos_num = len(cards_combos)
        grid_num = len(grids)
        
        for i in range(min(combos_num, grid_num)):
            combo = cards_combos[i]
            row, col = grids[i]
            self.place_cards_to_one_cell(combo, row, col)
            
        
        self.game_engine.current_player.hands = [card for card in self.game_engine.current_player.hands if card not in all_combos_cards]
        self.reset_drag_parameters()
        self.set_current_player_hands()
        self.grid_cards = {k: v for k, v in self.grid_cards.items() if v != []}
        self.sort_grid(self.grid_cards)
        self.game_engine.current_player.made_move = True
        return True