import pygame
import random

from config import *

class Timer:
    def __init__(self,max_time = MAX_TIME):
        self.initial_time = pygame.time.get_ticks() // 1000
        self.objects = []
        self.image_dict = self.load_image()
        self.max_time = max_time
        self.x = 1050
        self.y = 600
        self.first_rect = None
        self.initial_score = None

    def display(self, game_ui):
        time_passed_in_seconds = pygame.time.get_ticks() // 1000 - self.initial_time
        time_left = self.max_time - time_passed_in_seconds
        if time_left < 0:
            if self.initial_score is None:
                self.initial_score = game_ui.game_engine.current_player.score
            game_ui.notification = "Time's up!"
            game_ui.game_engine.current_player.score = self.initial_score + time_left
            
        str_seconds = str(time_left) if time_left > 0 else "jjj"
        if len(str_seconds) != 3:
            str_seconds = (3-len(str_seconds))*"0" + str_seconds

        for i in range(len(str_seconds)):
            image = self.get_object(str_seconds[i])
            if i == 0:
                self.first_rect = image.get_rect()
                self.first_rect.x += self.x + 2*GAP
                self.first_rect.y += self.y
            game_ui.screen.blit(image, (self.first_rect.x + (i*(CARD_WIDTH)), self.first_rect.y))
        text = pygame.font.SysFont(None, 24).render(f"Time remaning (seconds)", True, (255, 255, 255)) 
        game_ui.screen.blit(text, (self.first_rect.x - 2*GAP, self.first_rect.y + 75))
        
    
    def load_image(self):
        dict_str_to_image = {}
        colour = random.choice(ALL_COLOURS).lower()
        dict_str_to_image["j"] = pygame.transform.smoothscale(pygame.image.load("./src/finalcards/joker.png"), (CARD_WIDTH, CARD_HEIGHT))
        for number in range(10):
            if number != 0:
                path = f"./src/finalcards/red-{number}.png"
                dict_str_to_image[str(number)] = pygame.transform.smoothscale(pygame.image.load(path), (CARD_WIDTH, CARD_HEIGHT))
            else:
                path = f"./src/finalcards/back.png"
                dict_str_to_image[str(number)] = pygame.transform.smoothscale(pygame.image.load(path), (CARD_WIDTH, CARD_HEIGHT))
        return dict_str_to_image
        
    def get_object(self,number: str):
        return self.image_dict[number]
        
