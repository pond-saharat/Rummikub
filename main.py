import pygame
import random
import card
import sys

from pygame.locals import *
from surface import *
# Pygame constants and variables
HEIGHT = 450
WIDTH = 400
FPS = 60

# Pygame interface
pygame.init()
displaysurface  = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Rummikub")
FramePerSec = pygame.time.Clock()

# Game constants and variables
pool = card.CardPool()

# Add elements
card_test = CardSurface()
sprites = pygame.sprite.Group()
sprites.add(card_test)
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
     
    displaysurface.fill((0,0,0))
 
    for sprite in sprites:
        displaysurface.blit(sprite.surf, sprite.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

