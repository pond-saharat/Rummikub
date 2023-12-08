import pygame
import button
from config import *
import game_ui


# Menu class 
class Menu:
    #define the color of the text
    TEXT_COL = (255, 255, 255)

    def __init__(self, game_ui):
        #synchronize the screen with game_ui
        self.game_ui = game_ui
        pygame.display.set_caption("Main Menu")
        self.screen = self.game_ui.screen
        #The menu_state track the which part of the screen should be open
        self.menu_state = "main"
        self.game_paused = False
        # define fonts
        self.font = pygame.font.SysFont("arialblack", 40)
        #define the position of the volume control bar
        self.VPOS = SCREEN_WIDTH//2
        self.scale = 1.5

    def run(self,game_paused=False,finish=False) -> None:
        if finish:
            self.menu_state = "Rummikub!"
        self.game_paused=game_paused
        if self.game_paused == True:
            self.menu_state = "pause"
        background = pygame.image.load("image/background1.png").convert_alpha()
        #Load the image of background, congradulation and university logo
        background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        backgroundtwo = pygame.image.load("image/background2.png").convert_alpha()
        backgroundtwo = pygame.transform.smoothscale(backgroundtwo, (SCREEN_WIDTH, SCREEN_HEIGHT))
        logo = pygame.image.load("image/logo.png").convert_alpha()
        logo = pygame.transform.smoothscale(logo, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        #define buttons
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
        

        # load music
        pygame.mixer_music.load("image/Never.WAV")
        pygame.mixer.music.play(-1)
        # game loop
        running = True
        while running:
            #draw the screen
            self.screen.fill(BACKGROUND_COLOUR)
            self.screen.blit(background, (0, 0))
            self.screen.blit(logo, (SCREEN_WIDTH//2 - logo.get_rect().width //2, SCREEN_HEIGHT//2 - logo.get_rect().height//2 - 3 * BUTTON_GAP))
            #check the different state of menu 
            #The introduce interface
            if self.menu_state == "main" and self.game_ui.pause_state != True:
                #play a new game when use play_button
                if play_button.draw(self.screen):
                    self.menu_state = "choose_player"
                    running = True
                    pygame.time.delay(DELAY_TIME)
                #make the options when use option_button
                if options1_button.draw(self.screen):
                    self.game_paused = False
                    self.menu_state = "options"
                    pygame.time.delay(DELAY_TIME)
                #quit the game when use quit_button
                if quit_button1.draw(self.screen):
                    self.game_ui.running = False
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
            # The interface to choose how many ai or human players
            elif self.menu_state == "choose_player" and self.game_ui.pause_state != True:
                #No human player
                if zero_player_button.draw(self.screen):
                    self.game_ui.num_of_ais = 4
                    self.game_ui.num_of_humans = 0
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                #One human player
                if one_player_button.draw(self.screen):
                    self.game_ui.num_of_ais = 3
                    self.game_ui.num_of_humans = 1
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                #two human player
                if two_players_button.draw(self.screen):
                    self.game_ui.num_of_ais = 2
                    self.game_ui.num_of_humans = 2
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                #Three human player
                if three_players_button.draw(self.screen):
                    self.game_ui.num_of_ais = 1
                    self.game_ui.num_of_humans = 3
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                #Four human player
                if four_players_button.draw(self.screen):
                    self.game_ui.num_of_ais = 0
                    self.game_ui.num_of_humans = 4
                    self.game_ui.game_state = "game"
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
            #The interface when player pause the game
            elif self.menu_state == "pause":
                # Return to the game playing
                if resume_button.draw(self.screen):
                    self.game_ui.game_state = "game"
                    running = False
                    pygame.time.delay(DELAY_TIME)
                #going into the option interface
                if options_button.draw(self.screen):
                    self.menu_state = "options"
                    running = True
                    pygame.time.delay(DELAY_TIME)
                    print("This is called 3")
                #Quit the game    
                if quit_button.draw(self.screen):
                    self.game_ui.running = False
                    running = False
                    pygame.time.delay(DELAY_TIME)
            #The option interface
            elif self.menu_state == "options":  
                #going to the music setting option              
                if audio_button.draw(self.screen):
                    self.menu_state = "music"
                    pygame.time.delay(DELAY_TIME)  
                #return to the pervious interface                 
                if back_button.draw(self.screen):
                    #if player enter this interface through the pause interface, return to the pause interace
                    if self.game_paused == True:
                        self.menu_state = "pause"
                        pygame.time.delay(DELAY_TIME)
                    #if player enter this interface through the main interface, return to the main interace    
                    if self.game_paused == False:
                        self.menu_state = "main"
                        pygame.time.delay(DELAY_TIME)
            #The music setting interface            
            elif self.menu_state == "music":
                #back to the option interface
                if back_button.draw(self.screen):
                    self.menu_state = "options"
                    pygame.time.delay(DELAY_TIME)
                #set the volume control bar
                pygame.draw.line(self.screen, (255, 255, 255), (SCREEN_WIDTH//2 - BUTTON_WIDTH, SCREEN_HEIGHT//2), (SCREEN_WIDTH//2+ BUTTON_WIDTH, SCREEN_HEIGHT//2), 5)
               #The volume control button
                self.volume_button = pygame.draw.circle(self.screen, (255, 255, 0), (self.VPOS, SCREEN_HEIGHT//2), 10, width=0)
                volume_state = 0
                # player can change the volume only they click the mouse
                if pygame.mouse.get_pressed()[0]:
                    if self.volume_button.collidepoint(pygame.mouse.get_pos()):
                        volume_state = 1
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and volume_state:
                        volume_state = 0
                # Track the position of the mouse
                pos = pygame.mouse.get_pos()
                #Restrict the volume botton on the volume control bar
                if volume_state:
                    self.VPOS = pos[0]
                    if self.VPOS > SCREEN_WIDTH//2 + BUTTON_WIDTH:
                        self.VPOS = SCREEN_WIDTH//2 + BUTTON_WIDTH
                    elif self.VPOS < SCREEN_WIDTH//2 - BUTTON_WIDTH:
                        self.VPOS = SCREEN_WIDTH//2 - BUTTON_WIDTH
                    else:
                        pass
                    #change the volume 
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
            # The congratulation pages when a player have win the game        
            elif self.menu_state == "Rummikub!":
                #set a different background
                self.screen.fill(BACKGROUND_COLOUR)
                self.screen.blit(backgroundtwo, (0, 0))
                #Show which player win the game and how many point he win
                text_surface = self.font.render(f'Congratulations!', True, (255, 255, 255))
                self.screen.blit(text_surface, (SCREEN_WIDTH//2-text_surface.get_rect().width//2,SCREEN_HEIGHT//2-text_surface.get_rect().height//2-BUTTON_GAP))
                text_surface = self.font.render(f'{self.game_ui.game_engine.winners[0]} is a winner with a score of {self.game_ui.game_engine.winning_score}', True, (255, 255, 255))
                self.screen.blit(text_surface, (SCREEN_WIDTH//2-text_surface.get_rect().width//2,SCREEN_HEIGHT//2-text_surface.get_rect().height//2))
                #quit the game
                if quit_button1.draw(self.screen):
                    self.game_ui.running = False
                    running = False
                    self.game_paused = True
                    pygame.time.delay(DELAY_TIME)
                    pygame.quit()
                    exit()
            else:
                pass
            
            # event handler
            for event in pygame.event.get():
                #push space to pause the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_paused = True
                        self.menu_state = "pause"
                #quit the game if click the quit
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
        #Entering the game    
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