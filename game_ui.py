import pygame
import game_engine

from pygame.locals import *
from config import *

class GameUI:
    def __init__(self):
        self.running = True
        # Initialize an empty group of game objects
        self.sprites = pygame.sprite.Group()
        # Refer ui engine location to ui game location and refer game engine location to ui engine location
        self.game_engine = game_engine.GameEngine(self)
        
    # Run the game loop
    def run(self):
        pygame.init()
        pygame.mouse.set_visible(1)
        # Create a blank screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.screen.fill("white")
        # Add all sprites
        self.add_all_sprites()
        # Infinite loop
        while self.running:
            # Check the inputs provided by the user
            for event in pygame.event.get():
                self.check_event(event)
            # Clear the screen
            self.screen.fill("white")
            # Draw all of the sprites
            self.sprites.draw(self.screen)
            pygame.display.flip()

    def add_all_sprites(self):
        for obj in self.engine.objects:
            self.sprites.add(obj)

    def check_event(self,event):
        # Quit the game if the event is QUIT
        if event.type == pygame.QUIT:
            self.running = False
            return
        # Check for mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for obj in self.objects:
                # Check if the mouse click is within sprites' boundaries
                if obj.rect.collidepoint(mouse_x, mouse_y):
                    # Do the actions
                    obj.perform_action()
