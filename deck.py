import pygame
import random
import card

from config import *


# Class Deck
class Deck:
    def __init__(self):
        self.deck = []
        # Create a list of ColourCard instances
        self.deck += [
            card.ColourCard(colour, number)
            for colour in COLOURS
            for number in range(1, NUM_OF_CARDS_EACH_COLOUR + 1)
            for _ in range(NUM_OF_IDENTICAL_CARDS)
        ]
        # Create a list of JokerCard instances
        self.deck += [card.JokerCard() for _ in range(NUM_OF_JOKER_CARDS)]
        random.shuffle(self.deck)

    def __str__(self):
        return str(self.deck)
    
    def __repr__(self):
        return self.__str__()


# # For testing purposes
# d = Deck()
# print(d.deck[0].image)
