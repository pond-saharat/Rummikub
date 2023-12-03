import pygame
import button
from config import *

# Menu class
class Menu:
  TEXT_COL = (255, 255, 255)

  def __init__(self, game_ui):
    self.game_ui = game_ui
    pygame.display.set_caption("Rummikub - Paused")
    self.menu_state = "main"
    self.screen = self.game_ui.screen
    self.game_paused = False
    # define fonts
    self.font = pygame.font.SysFont("arialblack", 40)

  def run(self) -> None:
    #load button images
    resume_img = pygame.image.load("image/button_resume.png").convert_alpha()
    options_img = pygame.image.load("image/button_options.png").convert_alpha()
    quit_img = pygame.image.load("image/button_quit.png").convert_alpha()
    video_img = pygame.image.load('image/button_video.png').convert_alpha()
    audio_img = pygame.image.load('image/button_audio.png').convert_alpha()
    keys_img = pygame.image.load('image/button_keys.png').convert_alpha()
    back_img = pygame.image.load('image/button_back.png').convert_alpha()
    image1=pygame.image.load("image/uon.jpg").convert_alpha()

    #create button instances
    resume_button = button.Button(304, 125, resume_img, 1)
    options_button = button.Button(297, 250, options_img, 1)
    quit_button = button.Button(336, 375, quit_img, 1)
    video_button = button.Button(226, 75, video_img, 1)
    audio_button = button.Button(225, 200, audio_img, 1)
    keys_button = button.Button(246, 325, keys_img, 1)
    back_button = button.Button(332, 450, back_img, 1)

    #game loop
    running = True
    while running:
      self.screen.blit(image1,(0,0))
      # self.screen.fill((0,0, 255))

      #check if game is paused
      if self.game_paused == True:
        #check menu state
        if self.menu_state == "main":
          #draw pause screen buttons
          if resume_button.draw(self.screen):
            self.game_paused = False
          if options_button.draw(self.screen):
            self.menu_state = "options"
          if quit_button.draw(self.screen):
            running = False
        #check if the options menu is open
        if self.menu_state == "options":
          #draw the different options buttons
          if video_button.draw(self.screen):
            print("Video Settings")
          if audio_button.draw(self.screen):
            print("Audio Settings")
          if keys_button.draw(self.screen):
            print("Change Key Bindings")
          if back_button.draw(self.screen):
            self.menu_state = "main"
      else:
        self.draw_text("Press SPACE to pause", self.font, Menu.TEXT_COL, 160, 250)

      #event handler
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            self.game_paused = True
        if event.type == pygame.QUIT:
          running = False
          
          
      pygame.display.update()
    self.game_ui.game_state = "game"

  # Draw plain text on the center of the screen
  def draw_text(self, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    self.screen.blit(img, (x, y))
