import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self, colour, number):
        super().__init__()
        self.colour = colour
        self.number = number
        self.is_selected = False

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
    # None -> None
    def perform_action(self,game_engine):
        # Add itself to the list of selected cards
        game_engine.current_turn.selected_cards += self
        self.is_highlighted = not self.is_highlighted

    # Get only the colour cards for a pack of cards
    # None -> List[ColourCard]
    @staticmethod
    def get_colour_cards(cards):
        return [colour_card for colour_card in cards if isinstance(colour_card, ColourCard)]

    # Get only the colour cards for a pack of cards
    # None -> List[JokerCard]
    @staticmethod
    def get_joker_cards(cards):
        return [colour_card for colour_card in cards if isinstance(colour_card, ColourCard)]
    

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