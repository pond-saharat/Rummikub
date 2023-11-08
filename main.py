import pygame
import random

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

# Add elements
engine = Engine()
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Fill the background
    displaysurface.fill((0,0,0))

    for sprite in engine.draw():
        displaysurface.blit(sprite.surf, sprite.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)

