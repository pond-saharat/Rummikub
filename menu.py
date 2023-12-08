import pygame

import button
import game_ui
from config import *

# Menu class
class Menu:
    TEXT_COL = (255, 255, 255)
    def __init__(self, game_ui):
        self.game_ui = game_ui
        pygame.display.set_caption("Main Menu")
        self.menu_state = "main"
        self.screen = self.game_ui.screen
        self.game_paused = False
        # define fonts
        self.font = pygame.font.SysFont("arialblack", 40)
        self.VPOS = SCREEN_WIDTH//2
        self.scale = 1.5
    
    # Running a menu
    # None -> None
    def run(self,game_paused=False,finish=False) -> None:
        # Check if the game is finished
        if finish:
            self.menu_state = "Rummikub!"
        self.game_paused=game_paused
        if self.game_paused == True:
            self.menu_state = "pause"

        # Load background and logo images
        background = pygame.image.load("image/background1.png").convert_alpha()
        background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        backgroundtwo = pygame.image.load("image/background2.png").convert_alpha()
        backgroundtwo = pygame.transform.smoothscale(backgroundtwo, (SCREEN_WIDTH, SCREEN_HEIGHT))
        logo = pygame.image.load("image/logo.png").convert_alpha()
        logo = pygame.transform.smoothscale(logo, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

        # Load buttons
        quit_button1 = button.Button(FIFTH_BUTTON_REGION, "Quit")
        play_button = button.Button(THIRD_BUTTON_REGION, "Play")
        options1_button = button.Button(FOURTH_BUTTON_REGION, "Option")
        resume_button = button.Button(THIRD_BUTTON_REGION,"Resume")
        options_button = button.Button(FOURTH_BUTTON_REGION, "Option")
        quit_button = button.Button(FIFTH_BUTTON_REGION, "Quit")
        video_button = button.Button(THIRD_BUTTON_REGION, "Video setting")
        audio_button = button.Button(FOURTH_BUTTON_REGION, "Audio setting")
        back_button = button.Button(FIFTH_BUTTON_REGION, "Back")
        zero_player_button = button.Button(FIRST_BUTTON_REGION, "Watch AIs playing")
        one_player_button = button.Button(SECOND_BUTTON_REGION, "1 Player")
        two_players_button = button.Button(THIRD_BUTTON_REGION, "2 Players")
        three_players_button = button.Button(FOURTH_BUTTON_REGION, "3 Players")
        four_players_button = button.Button(FIFTH_BUTTON_REGION, "4 Players")
        

        # Load music
        pygame.mixer_music.load("image/Never.WAV")
        pygame.mixer.music.play(-1)

        # Game loop
        running = True
        while running:
            self.screen.fill(BACKGROUND_COLOUR)
            self.screen.blit(background, (0, 0))
            self.screen.blit(logo, (SCREEN_WIDTH//2 - logo.get_rect().width //2, SCREEN_HEIGHT//2 - logo.get_rect().height//2 - 3 * BUTTON_GAP))
           
            # Check if the menu state is "main"
            if self.menu_state == "main" and self.game_ui.pause_state != True:
                if play_button.draw(self.screen):
                    self.menu_state = "choose_player"
                    running = True
                    pygame.time.delay(DELAY_TIME)
                if options1_button.draw(self.screen):
                    self.game_paused = False
                    self.menu_state = "options"
                    pygame.time.delay(DELAY_TIME)
                if quit_button1.draw(self.screen):
                    self.game_ui.running = False
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)

            # Check if the menu state is "choose_player"
            elif self.menu_state == "choose_player" and self.game_ui.pause_state != True:
                if zero_player_button.draw(self.screen):
                    self.game_ui.num_of_ais = 4
                    self.game_ui.num_of_humans = 0
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                if one_player_button.draw(self.screen):
                    self.game_ui.num_of_ais = 3
                    self.game_ui.num_of_humans = 1
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                if two_players_button.draw(self.screen):
                    self.game_ui.num_of_ais = 2
                    self.game_ui.num_of_humans = 2
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                if three_players_button.draw(self.screen):
                    self.game_ui.num_of_ais = 1
                    self.game_ui.num_of_humans = 3
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                if four_players_button.draw(self.screen):
                    self.game_ui.num_of_ais = 0
                    self.game_ui.num_of_humans = 4
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
            # Check if the menu state is "pause"
            elif self.menu_state == "pause":
                if resume_button.draw(self.screen):
                    self.game_ui.game_state = "game"
                    running = False
                    pygame.time.delay(DELAY_TIME)
                if options_button.draw(self.screen):
                    self.menu_state = "options"
                    running = True
                    pygame.time.delay(DELAY_TIME)
                if quit_button.draw(self.screen):
                    self.game_ui.running = False
                    running = False
                    pygame.time.delay(DELAY_TIME)
            # Check if themenu state is "options"
            elif self.menu_state == "options":     
                if audio_button.draw(self.screen):
                    self.menu_state = "music"
                    pygame.time.delay(DELAY_TIME)
                if back_button.draw(self.screen):
                    if self.game_paused == True:
                        self.menu_state = "pause"
                        pygame.time.delay(DELAY_TIME)
                    if self.game_paused == False:
                        self.menu_state = "main"
                        pygame.time.delay(DELAY_TIME)
            # Check if themenu state is "music"
            elif self.menu_state == "music":
                if back_button.draw(self.screen):
                    self.menu_state = "options"
                    pygame.time.delay(DELAY_TIME)
                pygame.draw.line(self.screen, (255, 255, 255), (SCREEN_WIDTH//2 - BUTTON_WIDTH, SCREEN_HEIGHT//2), (SCREEN_WIDTH//2+ BUTTON_WIDTH, SCREEN_HEIGHT//2), 5)
                self.volume_button = pygame.draw.circle(
                    self.screen, (255, 255, 0), (self.VPOS, SCREEN_HEIGHT//2), 10, width=0
                )
                volume_state = 0
                if pygame.mouse.get_pressed()[0]:
                    if self.volume_button.collidepoint(pygame.mouse.get_pos()):
                        volume_state = 1
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and volume_state:
                        volume_state = 0
                pos = pygame.mouse.get_pos()
                if volume_state:
                    self.VPOS = pos[0]
                    if self.VPOS > SCREEN_WIDTH//2 + BUTTON_WIDTH:
                        self.VPOS = SCREEN_WIDTH//2 + BUTTON_WIDTH
                    elif self.VPOS < SCREEN_WIDTH//2 - BUTTON_WIDTH:
                        self.VPOS = SCREEN_WIDTH//2 - BUTTON_WIDTH
                    else:
                        pass
                    Vlm = self.VPOS
                    Volume = (self.VPOS-(SCREEN_WIDTH//2-(SCREEN_WIDTH//2 - BUTTON_WIDTH))) / (SCREEN_WIDTH//2)
                    pygame.mixer.music.set_volume(Volume-0.25)
                    self.volume_button = pygame.draw.circle(
                        self.screen, (255, 255, 0), (self.VPOS, SCREEN_HEIGHT//2), 10, width=0
                    )
                else:
                    self.volume_button = pygame.draw.circle(
                        self.screen, (255, 255, 0), (self.VPOS, SCREEN_HEIGHT//2), 10, width=0
                    )
            # Check if themenu state is "Rummikub!"
            elif self.menu_state == "Rummikub!":
                self.screen.fill(BACKGROUND_COLOUR)
                self.screen.blit(backgroundtwo, (0, 0))
                text_surface = self.font.render(f'Congratulations!', True, (255, 255, 255))
                self.screen.blit(text_surface, (SCREEN_WIDTH//2-text_surface.get_rect().width//2,SCREEN_HEIGHT//2-text_surface.get_rect().height//2-BUTTON_GAP))
                text_surface = self.font.render(f'{self.game_ui.game_engine.winners[0]} is a winner with a score of {self.game_ui.game_engine.winning_score}', True, (255, 255, 255))
                self.screen.blit(text_surface, (SCREEN_WIDTH//2-text_surface.get_rect().width//2,SCREEN_HEIGHT//2-text_surface.get_rect().height//2))
                if quit_button1.draw(self.screen):
                    self.game_ui.running = False
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                    pygame.quit()
                    exit()
            else:
                pass
            
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_paused = True
                        self.menu_state = "pause"

                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
        # Drawing a loading screen when the game loop ends
        self.game_ui.game_state = "game"
        self.screen.fill(BACKGROUND_COLOUR)
        self.screen.blit(backgroundtwo, (0, 0))
        text_surface = self.font.render('Loading ...', True, (255, 255, 255))
        self.screen.blit(text_surface, (SCREEN_WIDTH//2-text_surface.get_rect().width//2,SCREEN_HEIGHT//2-text_surface.get_rect().height//2))
        pygame.display.update()

    # Draw plain text on the center of the screen
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
