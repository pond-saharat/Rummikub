import pygame
import card as c
import bot
import cardset
from config import *

# This file contains class Button and class GameButton. The difference is that Button can return the value. 
# On the other hand, GameButton is encapsulated with methods such as GameButton.left_click_action().

# Button class
class Button(pygame.sprite.Sprite):
    def __init__(self, rect,text, size=36):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.font = pygame.font.SysFont(None, 36)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.size = size
        self.message = text
        self.text = self.font.render(text, True, 0)
        self.text_rect = self.text.get_rect(center=(self.rect.x + (self.width//2), self.rect.y + (self.height//2)))
        self.radius = 15
        self.clicked = False
        self.hover = False
        self.visible = False
    
    # Draw a button and retrive the action in bool if the button is clicked
    # Display Surface object -> bool
    def draw(self, screen):
        action = False
        # Get the mouse position
        pos = pygame.mouse.get_pos()
        # Draw a shadow surface
        shadow = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_rect = shadow.get_rect()
        pygame.draw.rect(shadow,(16, 38, 59, 100),shadow_rect, border_radius=self.radius)

        # Set an offset to a shadow Rect object
        offset = 3
        shadow_rect.x = self.rect.x + offset
        shadow_rect.y = self.rect.y + offset

        # Drawing shadow and a button
        screen.blit(shadow, (shadow_rect.x, shadow_rect.y))
        pygame.draw.rect(screen, (250, 246, 239), self.rect, border_radius=self.radius)

        # Check mouseover and clicked events
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw text on the button
        screen.blit(self.text, self.text_rect)
        return action

# GameButton class
class GameButton(pygame.sprite.Sprite):
    def __init__(self, rect, text, size=36):
        super().__init__()
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.font = pygame.font.SysFont(None, 36)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.size = size
        self.text = text
        self.text = self.font.render(self.text, True, 0)
        self.text_rect = self.text.get_rect(
            center=(self.rect.x + (self.width // 2), self.rect.y + (self.height // 2))
        )
        self.radius = 15
        self.clicked = False
        self.hover = False
        self.visible = False

    # Draw a button
    # Display Surface object -> bool
    def draw(self, screen):
        # Draw a shadow surface
        shadow = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_rect = shadow.get_rect()
        pygame.draw.rect(
            shadow, (16, 38, 59, 100), shadow_rect, border_radius=self.radius
        )

        # Set an offset to a shadow Rect object
        offset = 3
        shadow_rect.x = self.rect.x + offset
        shadow_rect.y = self.rect.y + offset

        # Drawing shadow and a button
        screen.blit(shadow, (shadow_rect.x, shadow_rect.y))
        if not self.clicked:
            pygame.draw.rect(
                screen, (250, 246, 239), self.rect, border_radius=self.radius
            )
        else:
            pygame.draw.rect(
                screen, (200, 194, 189), self.rect, border_radius=self.radius
            )

        # Drawing text on a button
        screen.blit(self.text, self.text_rect)

    # Define left_click_action of the parent class
    def left_click_action(self, game_ui):
        self.clicked = True
        pass

    # Define left_click_action of the parent class when MOUSEBUTTONUP event occurs.
    def left_click_up_action(self, game_ui):
        pass

# All game related buttons with specific functionality
# Draw button
class DrawButton(GameButton):
    def __init__(self, rect, text, size=36):
        super().__init__(rect, text, size)
        self.cards = []

    def left_click_action(self, game_ui):
        self.clicked = True
        deck = game_ui.game_engine.deck.deck
        region = game_ui.draw_region
        if len(deck) >= 2:
            card1, card2 = tuple(deck[:2])
            card1.visible = True
            card2.visible = True
            self.cards = [card1, card2]
            card1.rect.x, card1.rect.y = region.x + GAP, region.y + GAP
            card2.rect.x, card2.rect.y = region.x + GAP + CARD_WIDTH + GAP, region.y + GAP
        elif len(deck) == 1:
            card1 = deck[0]
            card1.visible = True
            self.cards = [card1]
            card1.rect.x, card1.rect.y = region.x + GAP, region.y + GAP
        else:
            game_ui.notification = "No more cards in the deck"
            return

    def reset(self):
        for card in self.cards:
            card.visible = False
        self.cards = []
        self.clicked = False

# End Turn button
class EndTurnButton(GameButton):
    def __init__(self, rect, text, size=36):
        super().__init__(rect, text, size)

    def left_click_action(self, game_ui):
        self.clicked = True
        if game_ui.game_engine.current_player.made_move == False:
            # if game_ui.grid_cards
            if not all(cardset.CardSet.is_valid(combo) for combo in game_ui.grid_cards.values()):
                game_ui.notification = "Invalid move to the grid"
                return
            game_ui.notification = "Need to make a move or draw"
            return
        game_ui.reset_drag_parameters()
        game_ui.game_engine.next_turn()
        print(f"It's now {game_ui.game_engine.current_player}'s turn")

# Flip All Cards button
class FlipAllCardsButton(GameButton):
    def __init__(self, rect, text, size=36):
        super().__init__(rect, text, size)

    def left_click_action(self, game_ui):
        self.clicked = True
        for player in [
            p
            for p in game_ui.game_engine.players
            if p != game_ui.game_engine.current_player
        ]:
            c.Card.flip_all_cards(player.hands)

# Play For Me button
class PlayForMeButton(GameButton):
    def __init__(self, rect, text, size=36):
        super().__init__(rect, text, size)

    def left_click_action(self, game_ui):
        self.clicked = True
    
    def left_click_up_action(self, game_ui):
        game_ui.play_for_me()

# Hint button
class HintButton(GameButton):
    def __init__(self, rect, text, size=36):
        super().__init__(rect, text, size)

    def left_click_action(self, game_ui):
        self.clicked = True
        game_ui.hand_cards_tensor = bot.CardsTensor(
            cards=game_ui.game_engine.current_player.hands
        )
        best_play_idx_combos, sum = game_ui.hand_cards_tensor.find_max_sum_combos_idx()
        all_indices = [i for combo in best_play_idx_combos for i in combo]
        cards_in_best_play = [
            game_ui.game_engine.current_player.hands[i] for i in all_indices
        ]
        c.Card.set_to_selected(cards_in_best_play, game_ui)
        game_ui.notification = f"Hint: {cards_in_best_play}" if cards_in_best_play else "No combos in hand"

        print(cards_in_best_play, f"The max sum: {sum}")
        print("selected: ", game_ui.selected_cards)
