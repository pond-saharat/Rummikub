import pygame
import game_engine
import board

from pygame.locals import *
from config import *


class GameUI:
    def __init__(self):
        self.running = True
        # Initialize an empty group of game objects
        self.sprites = pygame.sprite.Group()
        # Refer ui engine location to ui game location and refer game engine location to ui engine location
        self.game_engine = game_engine.GameEngine(self)
        pygame.init()
        # clock = pygame.time.Clock()

        pygame.mouse.set_visible(1)
        # Create a blank screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.game_engine.screen = self.screen

        # button settings
        self.button_font = pygame.font.SysFont(None, 36)
        self.button_rect = pygame.Rect(300, 100, 150, 50)
        self.button_text = self.button_font.render("End Turn", True, 0)
        # pygame.time.delay(100)

        # drag and drop settings
        self.dragging = False
        self.card_being_dragged = None
        self.offset_x = 0
        self.offset_y = 0
        self.grid_cards = board.Board().grid_cards  # { (row, col): [card1, card2, ...], ... }
        self.selected_cards = []

    # Run the game loop
    def run(self):
        self.screen.fill(BACKGROUND_COLOUR)
        # Add all sprites
        self.add_all_sprites()

        # deal cards
        self.game_engine.deal_cards()
        self.set_current_player_hands()

        # Infinite loop
        while self.running:
            # Check the inputs provided by the user
            for event in pygame.event.get():
                self.check_event(event)
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
                pygame.draw.rect(self.screen, 0, card.rect, 2)

            pygame.display.flip()

    def add_all_sprites(self):
        for obj in self.game_engine.objects:
            self.sprites.add(obj)

    def check_event(self, event):
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
                            # Do the actions for the left click
                            self.start_dragging(card, event.pos)
                            break
                            # obj.left_click_action(self.game_engine)
            elif event.button == 3:
                for obj in self.sprites:
                    # Check if the mouse click is within sprites' boundaries
                    if obj.rect.collidepoint(mouse_x, mouse_y):
                        # Do the actions for the right click
                        obj.right_click_action(self.game_engine)
            else:
                pass

        # handle dropping card
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:  # left button released
                self.drop_card()
        # handle dragging
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            if self.card_being_dragged is not None:
                mouse_x, mouse_y = event.pos
                new_x = mouse_x + self.offset_x
                new_y = mouse_y + self.offset_y

                # make sure the card is within the screen region
                new_x = max(0, new_x)
                new_y = max(0, new_y)
                new_x = min(SCREEN_WIDTH - self.card_being_dragged.rect.width, new_x)
                new_y = min(SCREEN_HEIGHT - self.card_being_dragged.rect.height, new_y)

                # update the card's position
                self.card_being_dragged.rect.x = new_x
                self.card_being_dragged.rect.y = new_y

                # self.screen.blit(self.card_being_dragged.surface, self.card_being_dragged.rect)
                self.card_being_dragged.draw(self.game_engine)

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
            grid_cards[_].sort(key=lambda crd: (crd.colour, crd.number))
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
        self.game_engine.current_player.hands.sort(
            key=lambda crd: (crd.colour, crd.number)
        )
        for i, card in enumerate(self.game_engine.current_player.hands):
            card.rect.centerx = 300 + CARD_WIDTH * i + 5 * i + 5
            card.rect.centery = 1100
            # card.draw(self.game_engine)

    def start_dragging(self, card, mouse_pos):
        self.dragging = True
        self.card_being_dragged = card
        self.offset_x = card.rect.x - mouse_pos[0]
        self.offset_y = card.rect.y - mouse_pos[1]
        # record the original position of the card
        self.original_grid = (self.find_nearest_grid(card.rect.centerx, card.rect.centery))
        self.original_x, self.original_y = (
            card.rect.centerx,
            card.rect.centery,
        )

    def drop_card(self):
        self.dragging = False
        # find the nearest grid to the card
        row, col = self.find_nearest_grid(self.card_being_dragged.rect.centerx, self.card_being_dragged.rect.centery)
        # add the new grid to the grid_cards if it is not in the grid_cards
        if (row, col) not in self.grid_cards.keys():
            self.grid_cards[(row, col)] = []


        ## if this is a valid position, put the card to the grid
        if self.is_valid_grid_position(row, col):
            ## if the card is still in the same grid, put it back to the original position of original grid
            if (row, col) == self.original_grid:
                self.card_being_dragged.rect.centerx = self.original_x
                self.card_being_dragged.rect.centery = self.original_y
                # control selected cards by clicking
                if self.card_being_dragged in self.selected_cards:
                    self.selected_cards.remove(self.card_being_dragged)
                else:
                    self.selected_cards.append(self.card_being_dragged)
            else:
                # update the card's position
                self.place_card_to_grid(self.card_being_dragged, row, col)

            # move selected cards to the grid
            # for i, selected_card in enumerate(selected_cards):
            #     selected_card.rect.x = grid_x + CARD_WIDTH * len(grid_cards[(row, col)]) + 5*len(grid_cards[(row, col)]) + 5 + CARD_WIDTH * i
            #     selected_card.rect.y = grid_y
            
        ## if the card is outside the board, put it back to the original position
        else:
            # row, col = original_row, original_col
            self.card_being_dragged.rect.centerx = self.original_x
            self.card_being_dragged.rect.centery = self.original_y
        
        self.card_being_dragged = None
        # remove empty keys and sort the cards in each grid
        self.grid_cards = {k: v for k, v in self.grid_cards.items() if v != []}
        self.sort_grid(self.grid_cards)
        print(self.grid_cards)
    
    def is_valid_grid_position(self, row, col):
        return 0 <= row < BOARD_HEIGHT // GRID_HEIGHT and 0 <= col < BOARD_WIDTH // GRID_WIDTH
    
    def place_card_to_grid(self, card, row, col):
        grid_x, grid_y = self.find_nearest_grid_pos(card.rect.centerx, card.rect.centery)
        card.rect.centerx = grid_x + CARD_WIDTH * len(self.grid_cards[(row, col)]) + 5 * len(self.grid_cards[(row, col)]) + 5
        card.rect.centery = grid_y
        # remove the card from the original grid if it is in the grid_cards
        if (self.original_grid in self.grid_cards.keys() and self.card_being_dragged in self.grid_cards[self.original_grid]):
            self.grid_cards[self.original_grid].remove(self.card_being_dragged)
        self.grid_cards[(row, col)].append(card)