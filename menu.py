import pygame
import button
import game_ui
from config import *

# Menu region
FIRST_BUTTON_REGION = ((SCREEN_WIDTH//2) - BUTTON_WIDTH//2, (SCREEN_HEIGHT//2) - BUTTON_HEIGHT//2 - 2* BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
SECOND_BUTTON_REGION = ((SCREEN_WIDTH//2) - BUTTON_WIDTH//2, (SCREEN_HEIGHT//2) - BUTTON_HEIGHT//2 - BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
THIRD_BUTTON_REGION = ((SCREEN_WIDTH//2) - BUTTON_WIDTH//2, (SCREEN_HEIGHT//2) - BUTTON_HEIGHT//2 , BUTTON_WIDTH, BUTTON_HEIGHT)
FOURTH_BUTTON_REGION = ((SCREEN_WIDTH//2) - BUTTON_WIDTH//2, (SCREEN_HEIGHT//2) - BUTTON_HEIGHT//2 + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
FIFTH_BUTTON_REGION = ((SCREEN_WIDTH//2) - BUTTON_WIDTH//2, (SCREEN_HEIGHT//2) - BUTTON_HEIGHT//2 + 2 * BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
# FLIP_ALL_CARDS_BUTTON_REGION = (BUTTON_X, BUTTON_Y + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
# PLAY_FOR_ME_BUTTON_REGION = (BUTTON_X, BUTTON_Y + 2 * BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
# HINT_BUTTON_REGION = (BUTTON_X, BUTTON_Y + 3 * BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
# DRAW_BUTTON_REGION = (BUTTON_X, BUTTON_Y + 4 * BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
class PlayButton(button.Button):
    def __init__(self, rect, text="Play",size=36):
        super().__init__(rect,text,size)

    def left_click_action(self, menu):
        self.clicked = True
        menu.running = False

        # Go to Loading page

class OptionButton(button.Button):
    def __init__(self, rect, text="Option",size=36):
        super().__init__(rect,text,size)

    def left_click_action(self, menu):
        self.clicked = True
        option_menu = OptionMenu(menu.game_ui)

class GameSettingButton(button.Button):
    def __init__(self, rect, text="Option",size=36):
        super().__init__(rect,text,size)

    def left_click_action(self, menu):
        self.clicked = True
        option_menu = OptionMenu(menu.game_ui)

class QuitButton(button.Button):
    def __init__(self, rect, text="Quit",size=36):
        super().__init__(rect,text,size)

    def left_click_action(self, menu):
        self.clicked = True
        pygame.quit()
        exit()

# class ResumeButton(button.Button):
#     def __init__(self, rect, text="Resume",size=36):
#         super().__init__(rect,text,size)

#     def left_click_action(self, menu):
#         self.clicked = True
class MainMenu:
    def __init__(self, game_ui):
        self.running = True
        self.game_ui = game_ui
        self.screen = self.game_ui.screen
        self.menu_state = "main_menu"
        self.sprites = pygame.sprite.Group()
        self.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.load_elements()
        self.load_buttons()

    def check_event(self,event):# Quit the game if the event is QUIT
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            self.running = False
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            if event.button == 1:
                for sprite in self.sprites:
                    if sprite.rect.collidepoint(mouse_x, mouse_y):
                        sprite.clicked = True
                        sprite.left_click_action(self)
            else:
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for sprite in self.sprites:
                    if sprite.rect.collidepoint(mouse_x, mouse_y):
                        sprite.clicked = False
        else:
            pass

    def load_elements(self):
        self.background_img = pygame.transform.smoothscale(
            pygame.image.load("./image/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    def load_buttons(self):
        self.sprites.add(PlayButton(THIRD_BUTTON_REGION))
        self.sprites.add(GameSettingButton(FOURTH_BUTTON_REGION))
        self.sprites.add(QuitButton(FIFTH_BUTTON_REGION))

    def run(self):
        # Music
        pygame.mixer_music.load("image/Never.WAV")
        pygame.mixer.music.play(-1)
        while self.running:

            for event in pygame.event.get():
                self.check_event(event)
            
            for sprite in self.sprites:
                sprite.draw(self.screen)

            pygame.display.flip()
    
    @classmethod
    def get_config(cls, game_ui):
        menu = cls(game_ui)
        menu.run()
        return

class OptionMenu(MainMenu):
    def __init__(self, game_ui):
        super().__init__(game_ui)
        self.menu_state = "main_menu"
        self.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.load_elements()
        self.load_buttons()
        
    def load_elements(self):
        self.background_img = pygame.transform.smoothscale(
            pygame.image.load("./image/background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

    def load_buttons(self):
        self.sprites.add(PlayButton(THIRD_BUTTON_REGION))
        self.sprites.add(OptionButton(FOURTH_BUTTON_REGION))
        self.sprites.add(QuitButton(FIFTH_BUTTON_REGION))
    
    def run(self):
        while self.running:

            for event in pygame.event.get():
                self.check_event(event)
            
            for sprite in self.sprites:
                sprite.draw(self.screen)

            pygame.display.flip()

        # # create button instances
        # resume_button = button.Button(304, 125, resume_img, 1)
        # options_button = button.Button(310, 320, options_img, 1)
        # options1_button = button.Button(500, 320, options_img, 1)
        # quit_button = button.Button(310, 520, quit_img, 1)
        # quit_button1 = button.Button(500, 520, quit_img, 1)
        # video_button = button.Button(226, 75, video_img, 1)
        # audio_button = button.Button(225, 200, audio_img, 1)
        # musicstop_button = button.Button(1000, 600, back_img, 1)
        # keys_button = button.Button(246, 325, keys_img, 1)
        # back_button = button.Button(332, 450, back_img, 1)
        # play_button = button.Button(500, 120, play_img, 1)


# # Menu class
# class Menu:
#     TEXT_COL = (255, 255, 255)

#     def __init__(self, game_ui):
#         self.game_ui = game_ui
#         pygame.display.set_caption("Main Menu")
#         self.menu_state = "main"
#         self.screen = self.game_ui.screen
#         self.game_paused = False
#         # define fonts
#         self.font = pygame.font.SysFont("arialblack", 40)
#         self.VPOS = 650
#         self.scale = 1.5

#     def run(self) -> None:
#         # load button images
#         play_img = pygame.image.load("image/button_play.png").convert_alpha()
#         play_img = pygame.transform.rotozoom(play_img, 0, self.scale)
#         resume_img = pygame.image.load("image/button_resume.png").convert_alpha()
#         resume_img = pygame.transform.rotozoom(resume_img, 0, self.scale)
#         options_img = pygame.image.load("image/button_options.png").convert_alpha()
#         options_img = pygame.transform.rotozoom(options_img, 0, self.scale)
#         quit_img = pygame.image.load("image/button_quit.png").convert_alpha()
#         quit_img = pygame.transform.rotozoom(quit_img, 0, self.scale)
#         video_img = pygame.image.load("image/button_video.png").convert_alpha()
#         audio_img = pygame.image.load("image/button_audio.png").convert_alpha()
#         keys_img = pygame.image.load("image/button_keys.png").convert_alpha()
#         back_img = pygame.image.load("image/button_back.png").convert_alpha()
#         image1 = pygame.image.load("image/uon.jpg").convert_alpha()

#         # create button instances
#         resume_button = button.Button(304, 125, resume_img, 1)
#         options_button = button.Button(310, 320, options_img, 1)
#         options1_button = button.Button(500, 320, options_img, 1)
#         quit_button = button.Button(310, 520, quit_img, 1)
#         quit_button1 = button.Button(500, 520, quit_img, 1)
#         video_button = button.Button(226, 75, video_img, 1)
#         audio_button = button.Button(225, 200, audio_img, 1)
#         musicstop_button = button.Button(1000, 600, back_img, 1)
#         keys_button = button.Button(246, 325, keys_img, 1)
#         back_button = button.Button(332, 450, back_img, 1)
#         play_button = button.Button(500, 120, play_img, 1)

#         # load music

#         # game loop
#         running = True
#         while running:
#             self.screen.blit(image1, (0, 0))
#             # self.screen.fill((0,0, 255))

#             # check if game is paused
#             # if self.game_paused == True or self.game_ui.pause_state==True:
#             # check menu state
#             if self.menu_state == "main" and self.game_ui.pause_state != True:
#                 # draw pause screen buttons
#                 self.draw_text(
#                     "Welcome to the Rummic game!", self.font, Menu.TEXT_COL, 400, 30
#                 )
#                 if play_button.draw(self.screen):
#                     self.game_ui.game_state = "game"
#                     running = False
#                     self.game_paused = True
#                 if options1_button.draw(self.screen):
#                     self.game_paused = False
#                     self.menu_state = "options"
#                 if quit_button1.draw(self.screen):
#                     self.game_ui.running = False
#                     running = False
#             if self.menu_state == "pause" or self.game_ui.pause_state == True:
#                 if resume_button.draw(self.screen):
#                     self.game_ui.game_state = "game"
#                     running = False
#                 # self.game_paused = False
#                 if options_button.draw(self.screen):
#                     self.menu_state = "options"
#                     self.game_paused = True
#                 if quit_button.draw(self.screen):
#                     self.game_ui.running = False
#                     running = False
#             # check if the options menu is open
#             if self.menu_state == "options":
#                 self.game_ui.pause_state = False
#                 # draw the different options buttons
#                 if video_button.draw(self.screen):
#                     print("Video Settings")
#                 if audio_button.draw(self.screen):
#                     self.menu_state = "music"
#                 if keys_button.draw(self.screen):
#                     print("Change Key Bindings")
#                 if back_button.draw(self.screen):
#                     if self.game_paused == True:
#                         self.menu_state = "pause"
#                     if self.game_paused == False:
#                         self.menu_state = "main"
#             if self.menu_state == "music":
#                 if quit_button1.draw(self.screen):
#                     self.menu_state = "options"
#                 

#             # event handler
#             for event in pygame.event.get():
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         self.game_paused = True
#                         self.menu_state = "pause"

#                 if event.type == pygame.QUIT:
#                     running = False

#             pygame.display.update()
#         self.game_ui.game_state = "game"

#     # Draw plain text on the center of the screen
#     def draw_text(self, text, font, text_col, x, y):
#         img = font.render(text, True, text_col)
#         self.screen.blit(img, (x, y))
