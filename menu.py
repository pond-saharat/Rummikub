import pygame
import button
from config import *
import game_ui


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
        self.VPOS = 650
        self.scale = 1.5

    def run(self) -> None:
        # load button images
        # play_img = pygame.image.load("image/button_play.png").convert_alpha()
        # play_img = pygame.transform.rotozoom(play_img, 0, self.scale)
        # resume_img = pygame.image.load("image/button_resume.png").convert_alpha()
        # resume_img = pygame.transform.rotozoom(resume_img, 0, self.scale)
        # options_img = pygame.image.load("image/button_options.png").convert_alpha()
        # options_img = pygame.transform.rotozoom(options_img, 0, self.scale)
        # quit_img = pygame.image.load("image/button_quit.png").convert_alpha()
        # quit_img = pygame.transform.rotozoom(quit_img, 0, self.scale)
        # video_img = pygame.image.load("image/button_video.png").convert_alpha()
        # audio_img = pygame.image.load("image/button_audio.png").convert_alpha()
        # keys_img = pygame.image.load("image/button_keys.png").convert_alpha()
        # back_img = pygame.image.load("image/button_back.png").convert_alpha()
        # image1 = pygame.image.load("image/uon.jpg").convert_alpha()
        # image1 = pygame.transform.scale(image1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        quit_button1 = button.Button(FIFTH_BUTTON_REGION, "Quit")

        # Main
        play_button = button.Button(THIRD_BUTTON_REGION, "Play")
        options1_button = button.Button(FOURTH_BUTTON_REGION, "Option")
        # create button instances
        resume_button = button.Button(THIRD_BUTTON_REGION,"Resume")
        options_button = button.Button(FOURTH_BUTTON_REGION, "Option")
        
        quit_button = button.Button(FIFTH_BUTTON_REGION, "Quit")
        
        video_button = button.Button(THIRD_BUTTON_REGION, "Video setting")
        audio_button = button.Button(THIRD_BUTTON_REGION, "Audio setting")
        # musicstop_button = button.Button(THIRD_BUTTON_REGION, "Music")
        keys_button = button.Button(THIRD_BUTTON_REGION, "Keys")
        back_button = button.Button(THIRD_BUTTON_REGION, "Back")
        

        # load music
        pygame.mixer_music.load("image/Never.WAV")
        pygame.mixer.music.play(-1)
        # game loop
        running = True
        while running:
            # self.screen.blit(image1, (0, 0))
            # self.screen.fill((0,0, 255))

            # check if game is paused
            # if self.game_paused == True or self.game_ui.pause_state==True:
            # check menu state
            if self.menu_state == "main" and self.game_ui.pause_state != True:
                # draw pause screen buttons
                # self.draw_text(
                #     "Welcome to the Rummic game!", self.font, Menu.TEXT_COL, 400, 30
                # )
                if play_button.draw(self.screen):
                    self.game_ui.game_state = "choose_player"
                    running = False
                    self.game_paused = True
                if options1_button.draw(self.screen):
                    self.game_paused = False
                    self.menu_state = "options"
                if quit_button1.draw(self.screen):
                    self.game_ui.running = False
                    running = False
            if self.menu_state == "choose_player" and self.game_ui.pause_state != True:
                pass
            if self.menu_state == "pause" or self.game_ui.pause_state == True:
                if resume_button.draw(self.screen):
                    self.game_ui.game_state = "game"
                    running = False
                # self.game_paused = False
                if options_button.draw(self.screen):
                    self.menu_state = "options"
                    self.game_paused = True
                if quit_button.draw(self.screen):
                    self.game_ui.running = False
                    running = False
            # check if the options menu is open
            if self.menu_state == "options":
                self.game_ui.pause_state = False
                # draw the different options buttons
                if video_button.draw(self.screen):
                    print("Video Settings")
                if audio_button.draw(self.screen):
                    self.menu_state = "music"
                if keys_button.draw(self.screen):
                    print("Change Key Bindings")
                if back_button.draw(self.screen):
                    if self.game_paused == True:
                        self.menu_state = "pause"
                    if self.game_paused == False:
                        self.menu_state = "main"
            if self.menu_state == "music":
                if quit_button1.draw(self.screen):
                    self.menu_state = "options"
                self.draw_text("Audio Changing", self.font, Menu.TEXT_COL, 500, 30)
                pygame.draw.line(self.screen, (255, 0, 0), (500, 300), (800, 300), 5)
                volume_button = pygame.draw.circle(
                    self.screen, (255, 255, 0), (self.VPOS, 300), 10, width=0
                )
                volume_state = 0
                if pygame.mouse.get_pressed()[0]:
                    if volume_button.collidepoint(pygame.mouse.get_pos()):
                        volume_state = 1
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and volume_state:
                        volume_state = 0
                pos = pygame.mouse.get_pos()
                if volume_state:
                    self.VPOS = pos[0]
                    if self.VPOS > 800:
                        self.VPOS = 800
                    elif self.VPOS < 300:
                        self.VPOS = 300
                    Vlm = self.VPOS
                    Volume = (self.VPOS - 500) / 300
                    pygame.mixer.music.set_volume(Volume)
                    self.volume_button = pygame.draw.circle(
                        self.screen, (255, 255, 0), (self.VPOS, 300), 10, width=0
                    )
                    print(Volume)
                else:
                    self.volume_button = pygame.draw.circle(
                        self.screen, (255, 255, 0), (self.VPOS, 300), 10, width=0
                    )

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_paused = True
                        self.menu_state = "pause"

                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
        self.game_ui.game_state = "game"

    # Draw plain text on the center of the screen
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))
