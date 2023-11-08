import pygame

class CardSurface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (10, 420))
