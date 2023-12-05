# Global variables
NUM_OF_CARDS_EACH_COLOUR = 13
NUM_OF_COLOURS = 5
ALL_COLOURS = ("Red", "Green", "Blue", "Yellow", "Pink")
COLOURS = ALL_COLOURS
NUM_OF_JOKER_CARDS = 2
NUM_OF_IDENTICAL_CARDS = 2
MAX_ROUND = 10
MAX_TIME = 100

NUM_OF_AI_PLAYERS = 0
NUM_OF_HUMAN_PLAYERS = 4

# Variables for GameEngine
REGENERATE_IMAGE = True

# Variables for GameUI
SET_SCREEN_WIDTH = 1280
SET_SCREEN_HEIGHT = 720

# Variables for GameUI
SCREEN_WIDTH = SET_SCREEN_WIDTH
SCREEN_HEIGHT = SET_SCREEN_HEIGHT
BACKGROUND_COLOUR = "#009BC1"
CAPTION = "Rummikub"

SCALE = 15
CARD_WIDTH = 684 // SCALE
CARD_HEIGHT = 955 // SCALE

GAP = CARD_WIDTH//3

GRID_WIDTH = CARD_WIDTH * 8 + 2 * GAP
GRID_HEIGHT = CARD_HEIGHT

HANDS_REGION = 100

# board region
BOARD_WIDTH = GRID_WIDTH * 2
BOARD_HEIGHT = GRID_HEIGHT * 8
