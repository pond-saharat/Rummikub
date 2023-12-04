import pygame
import game_engine
import menu
import board
import cardset

from pygame.locals import *
from config import *


class GameUI:
    def __init__(self):
        self.running = True
        # Initialize an empty group of game objects
        self.sprites = pygame.sprite.Group()

        pygame.init()
        # Create a blank screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Refer ui engine location to ui game location and refer game engine location to ui engine location
        self.game_engine = game_engine.GameEngine(self)

        # clock = pygame.time.Clock()

        pygame.mouse.set_visible(1)

        pygame.display.set_caption(CAPTION)
        # Passing screen to game_engine
        self.game_engine.screen = self.screen
        self.game_state = "main_menu"
    

        # button settings
        self.button_font = pygame.font.SysFont(None, 36)
        self.button_rect = pygame.Rect(1100, 20, 130, 50)
        self.button_text = self.button_font.render("Submit", True, 0)
        pygame.time.delay(10)

        # drag and drop settings
        self.dragging = False
        self.card_being_dragged = None
        self.offset_x = 0
        self.offset_y = 0
        self.grid_cards = board.Board().grid_cards # { (row, col): [card1, card2, ...], ... }
        self.selected_cards = self.game_engine.current_player.selected_cards

    # Run the game loop
    def run(self):
        self.screen.fill(BACKGROUND_COLOUR)
        # Add all sprites
        self.add_all_sprites()

        # deal cards
        # self.game_engine.deal_cards()
        self.set_current_player_hands()

        # Infinite loop
        while self.running:
            # Check the game state
            if self.game_state == "main_menu":
                menu.Menu(self).run()
            elif self.game_state == "game":
                # Check the inputs provided by the user
                for event in pygame.event.get():
                    self.check_event(event,self.game_engine)
                # Clear the screen
                self.screen.fill(BACKGROUND_COLOUR)
                # draw grid
                self.draw_grid(self.screen)
                # self.draw_hands_region()

                # draw button
                pygame.draw.rect(self.screen, (200, 200, 200), self.button_rect)
                self.screen.blit(
                    self.button_text, (self.button_rect.x + 20, self.button_rect.y + 10)
                )
                # Draw all of the sprites
                # self.set_current_player_hands()
                
                self.sprites.draw(self.screen)
                for card in self.selected_cards:
                    pygame.draw.rect(self.screen, 0, card.rect, 3)

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
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    self.game_engine.next_turn()
                    print(f"It's now {self.game_engine.current_player}'s turn")
                else:
                    for card in self.sprites:
                        # Check if the mouse click is within sprites' boundaries
                        if card.rect.collidepoint(mouse_x, mouse_y):
                            if card.owner == self.game_engine.current_player or card.owner is None:
                                # Do the actions for the left click
                                self.start_dragging(card, event.pos)
                                break
                                # obj.left_click_action(self.game_engine)
            elif event.button == 3:
                self.selected_cards = []
            else:
                pass

        # handle dropping card
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:  # left button released
                mouse_x, mouse_y = event.pos
                for card in self.sprites:
                    if (card.rect.collidepoint(event.pos) and mouse_x > CARD_WIDTH and mouse_y > CARD_HEIGHT):
                        # if the card is in the selected_cards, remove it from the selected_cards
                        if card in self.selected_cards:
                            self.selected_cards.remove(card)
                        else:
                            self.selected_cards.append(card)
                self.drop_card(game_engine)
        
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
                self.card_being_dragged.draw(self.game_engine)
        else:
            pass

    # Draw lines of the grid
    def draw_grid(self, screen):
        for x in range(HANDS_REGION, HANDS_REGION + BOARD_WIDTH + 1, GRID_WIDTH):
            pygame.draw.line(
                screen, 0, (x, HANDS_REGION), (x, HANDS_REGION + BOARD_HEIGHT)
            )
        for y in range(HANDS_REGION, HANDS_REGION + BOARD_HEIGHT + 1, GRID_HEIGHT):
            pygame.draw.line(
                screen, 0, (HANDS_REGION, y), (HANDS_REGION + BOARD_WIDTH, y)
            )

    def find_nearest_grid_pos(self, x, y):
        x_board = x - HANDS_REGION
        y_board = y - HANDS_REGION

        grid_x = x_board // GRID_WIDTH * GRID_WIDTH + CARD_WIDTH // 2 + HANDS_REGION
        grid_y = y_board // GRID_HEIGHT * GRID_HEIGHT + GRID_HEIGHT // 2 + HANDS_REGION
        return grid_x, grid_y

    def find_nearest_grid(self, x, y):
        x_board = x - HANDS_REGION
        y_board = y - HANDS_REGION

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
                    card.rect.centerx = card_grid_x + CARD_WIDTH * i + 5 * i + 5
                    card.rect.centery = card_grid_y
            else:
                grid_cards[_] = cardset.CardSet.sort_list(grid_cards[_])
                for i, card in enumerate(grid_cards[_]):
                    card_grid_x, card_grid_y = self.find_nearest_grid_pos(
                        card.rect.centerx, card.rect.centery
                    )
                    card.rect.centerx = card_grid_x + CARD_WIDTH * i + 5 * i + 5
                    card.rect.centery = card_grid_y

    def draw_hands_region(self):
        pygame.draw.rect(
            self.screen,
            0,
            (0, HANDS_REGION, HANDS_REGION, SCREEN_HEIGHT - 2 * HANDS_REGION),
            2,
        )
        pygame.draw.rect(
            self.screen,
            0,
            (HANDS_REGION, 0, SCREEN_WIDTH - 2 * HANDS_REGION, HANDS_REGION),
            2,
        )
        pygame.draw.rect(
            self.screen,
            0,
            (
                HANDS_REGION,
                SCREEN_HEIGHT - HANDS_REGION,
                SCREEN_WIDTH - 2 * HANDS_REGION,
                HANDS_REGION,
            ),
            2,
        )
        pygame.draw.rect(
            self.screen,
            0,
            (
                SCREEN_WIDTH - HANDS_REGION,
                HANDS_REGION,
                HANDS_REGION,
                SCREEN_HEIGHT - 2 * HANDS_REGION,
            ),
            2,
        )

    def set_current_player_hands(self):
        for p, player in enumerate(self.game_engine.players):
            player.hands.sort(key=lambda crd: (crd.colour, crd.number))
            if p == 0:
                for i, card in enumerate(player.hands):
                    card.rect.centerx = (HANDS_REGION + CARD_WIDTH * i + 5) + 5
                    card.rect.centery = HANDS_REGION + BOARD_HEIGHT + 50
            elif p == 1:
                i, j = 0, 0
                for card in player.hands:
                    card.rect.centerx = (HANDS_REGION + CARD_WIDTH * i + 5 * i + 5) - 70
                    card.rect.centery = HANDS_REGION + CARD_HEIGHT * j + 20
                    i += 1
                    if i == 2:
                        i = 0
                        j +=1
            elif p == 2:
                for i, card in enumerate(player.hands):
                    card.rect.centerx = HANDS_REGION + CARD_WIDTH * i + 5 * i + 5
                    card.rect.centery = HANDS_REGION - 50
            elif p == 3:
                i, j = 0, 0
                for card in player.hands:
                    card.rect.centerx = (HANDS_REGION + CARD_WIDTH * i + 5 * i + 5)  + BOARD_WIDTH + 30
                    card.rect.centery = HANDS_REGION + CARD_HEIGHT * j + 20
                    i += 1
                    if i == 2:
                        i = 0
                        j +=1
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
        self.dragging = False
        dropped_pos_x, dropped_pos_y = self.card_being_dragged.rect.centerx, self.card_being_dragged.rect.centery
        
        # If the current drop position is in current player's hand region -> leave a card in that region
        if game_engine.current_player.hand_region.collidepoint(dropped_pos_x, dropped_pos_y):
            for card in self.cards_being_dragged:
                if card not in game_engine.current_player.hands:
                    game_engine.current_player.hands.append(card)
                card.owner = game_engine.current_player
                if card in game_engine.deck.deck:
                    game_engine.deck.deck.remove(card)
            for key, card_list in self.grid_cards.items():
                self.grid_cards[key] = [crd for crd in card_list if crd not in self.cards_being_dragged]
            print("selected cards:", self.selected_cards)
            print("grid:", self.grid_cards)
            self.reset_drag_parameters()
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
                # remove the card from the original grid
                if (
                    original_grid in self.grid_cards
                    and card in self.grid_cards[original_grid]
                ):
                    self.grid_cards[original_grid].remove(card)
                # if the card is in the selected_cards, put all the selected cards to the grid
                self.place_card_to_grid(card, row, col)

                # Reset the owner of the card
                if card.owner:
                    card.owner.hands.remove(card)
                    card.owner = None

                card.owner = None

            ## if the card is outside the board, put it back to the original position
            else:
                card.rect.centerx = original_xy[0]
                card.rect.centery = original_xy[1]

        # Reset dragging parameters to their initial values
        self.reset_drag_parameters()

        # if all(card in self.grid_cards[(row, col)] for card in self.selected_cards):
        #     self.selected_cards = []
        # remove empty keys and sort the cards in each grid
        self.grid_cards = {k: v for k, v in self.grid_cards.items() if v != []}
        self.sort_grid(self.grid_cards)
        print("selected cards:", self.selected_cards)
        print("grid:", self.grid_cards)
        pygame.display.update()

    def reset_drag_parameters(self):
        self.game_engine.current_player.selected_cards = []
        for card in self.game_engine.current_player.hands:
            card.is_selected = False
        for k,cards in self.grid_cards.items():
            for card in cards:
                card.is_selected = False
        self.card_being_dragged = None
        self.cards_being_dragged = []
        self.original_positions = {}
        self.original_xy = {}
    
    def is_valid_grid_position(self, row, col):
        return (
            0 <= row < BOARD_HEIGHT // GRID_HEIGHT 
            and 0 <= col < BOARD_WIDTH // GRID_WIDTH 
        )


    def place_card_to_grid(self, card, row, col):
        grid_x, grid_y = self.find_nearest_grid_pos(
            card.rect.centerx, card.rect.centery
        )
        card.rect.centerx = (
            grid_x
            + CARD_WIDTH * len(self.grid_cards[(row, col)])
            + 5 * len(self.grid_cards[(row, col)])
            + 5
        )
        card.rect.centery = grid_y

        # if card not in self.grid_cards[(row, col)]:
        self.grid_cards[(row, col)].append(card)
        # self.selected_cards = []

    def show_players_hands(self):
        for player in self.game_engine.players:
            print(player.name, player.hands)
