import pygame,sys

NUM_OF_COLOURS = 4
NUM_OF_CARDS_EACH_COLOUR = 13
NUM_OF_WILDCARDS = 2
NUM_OF_SAME_CARD = 2

ALL_COLOURS = ("Red","Blue","Yellow","Green","Pink")
NOW_COLOURS = ALL_COLOURS[:NUM_OF_COLOURS]

print(NOW_COLOURS)

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# color = pygame.Color(r, g, b, a=255)

# for k, v in THECOLORS.items():
#    pygame.THECOLORS[sys.unicode_(k)] = v