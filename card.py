import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self, colour, number):
        super().__init__()
        self.colour = colour
        self.number = number
        self.is_selected = False
        self.parent_set = None

    def __repr__(self):
        return f"Card({self.colour} {self.number})"
        
    # Draw a card
    # Pygame Display object, Tuple(position_x, position_y) -> None
    def draw(self,screen,pos):
        if self.is_selected:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)
        else:
            screen.blit(self.image, pos)
    
    # Perfome actions when the card is clicked
    # Game engine instance -> None
    def left_click_action(self,game_engine):
        current_player = game_engine.turn
        # Actions if the card belongs to a set
        if self.parent_set:
            current_player.selected += self.parent_set
            self.parent_set.highlight()
        # Add itself to the list of selected cards
        else:
            current_player.selected += self
            self.highlight()
 

    # Perfome actions when the card is clicked
    # Game engine instance -> None
    def right_click_action(self,game_engine):
        current_player = game_engine.turn
        # Move to a set
        if self.parent_set:
            current_player.selected += self.parent_set
            current_player.make_move(game_engine)
        else:
            current_player.selected += self
            current_player.make_move(game_engine)

    # Highlight the card or unhighlight the card
    def highlight(self):
        self.is_selected = not self.is_selected

    # Get only the colour cards for a pack of cards
    # None -> List[ColourCard]
    @staticmethod
    def get_colour_cards(cards):
        return [colour_card for colour_card in cards if isinstance(colour_card, ColourCard)]

    # Get only the Joker cards for a pack of cards
    # None -> List[JokerCard]
    @staticmethod
    def get_joker_cards(cards):
        return [joker_card for joker_card in cards if isinstance(joker_card, JokerCard)]
    

class ColourCard(Card):
    def __init__(self, colour, number):
        super().__init__(colour, number)
        self.joker = False
        self.image = pygame.image.load(f"./src/{self.colour.lower()}{self.number}.png")
        self.rect = self.image.get_rect()

    # Get the penalty for this card 
    # None -> int
    def penalty(self):
        # Need to be implemented
        pass

class JokerCard(Card):
    def __init__(self):
        super().__init__(None, None)
        self.joker = True
        self.image = pygame.image.load(f"./src/joker.png")
        self.rect = self.image.get_rect()
    
    # Get the penalty for this card 
    # None -> int
    def penalty(self):
        return -30