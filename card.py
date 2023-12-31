import pygame
import os.path

from config import *

# Class Card
class Card(pygame.sprite.Sprite):
    def __init__(self, colour, number):
        super().__init__()
        self.colour = colour
        self.number = number
        self.is_selected = False
        self.parent_set = None
        self.flipped = True
        if os.path.isfile("./src/finalcards/back.png"):
            self.flipped_image_path = "./src/finalcards/back.png"
        else:
            self.flipped_image_path = "./src/cards/back.png"
        self.flipped_image = None
        self.visible = True
        # Owner is a Player object
        self.owner = None
        # Back side of the card
        self.back_image = None
        self.hover = False

    def __repr__(self):
        return f"{self.colour[0]}-{self.number}"

    # Update a sprite
    # Pygame Display object, Tuple(position_x, position_y) -> None
    def draw(self, screen):
        # Create a shadow surface
        shadow = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_rect = shadow.get_rect()
        shadow.fill((16, 38, 59, 100)) 

        # Add an offset to the Rect object of the shadow surface
        offset = 3
        shadow_rect.x = self.rect.x + offset
        shadow_rect.y = self.rect.y + offset

        # Draw a card based on the card's parameters such as visible, or flipped
        if self.visible:
            if self.flipped:
                screen.blit(shadow, (shadow_rect.x, shadow_rect.y))
                screen.blit(self.image, (self.rect.x, self.rect.y))
            else:
                screen.blit(shadow, (shadow_rect.x, shadow_rect.y))
                screen.blit(self.flipped_image, (self.rect.x, self.rect.y))


    # Perfome actions when the card is clicked
    # Game UI instance -> None
    def left_click_action(self, game_ui):
        pass
        # current_player = game_engine.current_player
        # # Actions if the card belongs to a set
        # if self.parent_set:
        #     current_player.selected_cards.append(self.parent_set)
        #     # print(current_player.selected_cards)
        #     self.parent_set.highlight(game_engine)
        # # Add itself to the list of selected cards
        # else:
        #     current_player.selected_cards.append(self)
        #     # print(current_player.selected_cards)

        #     self.highlight(game_engine)

    # Perfome actions when the card is clicked
    # Game engine instance -> None
    def right_click_action(self, game_engine):
        current_player = game_engine.current_player
        # Move to a set
        if self.parent_set:
            current_player.selected_cards.append(self.parent_set)
            current_player.make_move(game_engine)
        else:
            current_player.selected_cards.append(self)
            current_player.make_move(game_engine)
    
    def load_image(self):
        self.image = pygame.transform.smoothscale(
            pygame.image.load(self.image_path).convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)
        )
        # Flipped image
        self.flipped_image = pygame.transform.smoothscale(
            pygame.image.load(self.flipped_image_path).convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)
        )

    # Get only the colour cards for a pack of cards
    # None -> List[ColourCard]
    @staticmethod
    def get_colour_cards(cards):
        return [
            colour_card for colour_card in cards if isinstance(colour_card, ColourCard)
        ]

    # Get only the Joker cards for a pack of cards
    # None -> List[JokerCard]
    @staticmethod
    def get_joker_cards(cards):
        return [joker_card for joker_card in cards if isinstance(joker_card, JokerCard)]
    
    # Flip all cards
    # List[Card] -> None
    @staticmethod
    def flip_all_cards(cards):
        for card in cards:
            card.flipped = not card.flipped

    # Set to flipped
    # List[Card] -> None
    @staticmethod
    def set_to_flipped(cards):
        for card in cards:
            card.flipped = True
    
    # Set to umflipped
    # List[Card] -> None
    @staticmethod
    def set_to_unflipped(cards):
        for card in cards:
            card.flipped = False
    
    # Set cards of the player that is not the current player to unflipped
    @staticmethod
    def set_others_to_unflipped(game_engine):
        other_players = [player for player in game_engine.players if player != game_engine.current_player]
        for player in other_players:
            Card.set_to_unflipped(player.hands)

    # Get all penalty of all remaining cards
    # List[Card] -> int
    @staticmethod
    def get_penalty(cards):
        penalty = 0
        for card in cards:
            penalty += card.penalty()
        return penalty
    
    @staticmethod
    def set_to_selected(cards,game_ui):
        game_ui.selected_cards = cards
        for card in cards:
            card.is_selected = True

class ColourCard(Card):
    def __init__(self, colour, number):
        super().__init__(colour, number)
        self.joker = False
        if os.path.isfile(f"./src/finalcards/{self.colour.lower()}-{self.number}.png"):
            self.image_path = f"./src/finalcards/{self.colour.lower()}-{self.number}.png"
        else:
            self.image_path = f"./src/cards/{self.colour.lower()}-{self.number}.png"
        self.image = None
        self.load_image()
        self.rect = self.image.get_rect()

    # Get the penalty for this card
    # None -> int
    def penalty(self):
        return -self.number

class JokerCard(Card):
    def __init__(self):
        super().__init__("Joker", None)
        self.joker = True
        if os.path.isfile("./src/finalcards/joker.png"):
            self.image_path = "./src/finalcards/joker.png"
        else:
            self.image_path = "./src/cards/joker.png"
        self.image = None
        self.load_image()
        self.rect = self.image.get_rect()

    # Get the penalty for this card
    # None -> int
    def penalty(self):
        return -30
