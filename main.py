import game_ui
import button
import pygame
from config import *

winner_and_scores = {}
num_of_ais = 0
num_of_humans = 4

for num_of_game in range(MAX_GAME):
    if num_of_game == 0:
        game = game_ui.GameUI(num_of_game=num_of_game)
    else:
        game = game_ui.GameUI(num_of_game=num_of_game,num_of_ais=num_of_ais,num_of_humans=num_of_humans)
    score_and_winners,num_of_ais,num_of_humans = game.run()
    print(score_and_winners,num_of_ais,num_of_humans)
    for score in score_and_winners.keys():
        for winner in score_and_winners[score]:
            if winner not in winner_and_scores:
                winner_and_scores[winner] = score
            else:
                winner_and_scores[winner] += score

true_winner = max(winner_and_scores, key=winner_and_scores.get)
true_winning_score = winner_and_scores[true_winner]

pygame.init()
quit_button = button.Button(FIFTH_BUTTON_REGION, "Quit")
background = pygame.image.load("image/background1.png").convert_alpha()
# background = pygame.transform.smoothscale(backgroundtwo, (SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.transform.smoothscale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("arialblack", 40)
smallfont = pygame.font.SysFont("arialblack", 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.mixer_music.load("image/Never.WAV")
pygame.mixer.music.play(-1)
running = True
while running:
    screen.fill(BACKGROUND_COLOUR)
    screen.blit(background, (0, 0))
    # text_surface = font.render(f'Rummikub! Congratulations!', True, (255, 255, 255))
    # screen.blit(text_surface, (SCREEN_WIDTH//2-text_surface.get_rect().width//2,SCREEN_HEIGHT//2-text_surface.get_rect().height//2-BUTTON_GAP))
    text_surface = smallfont.render(f'{true_winner} is a winner with a score of {true_winning_score}', True, (255, 255, 255))
    screen.blit(text_surface, (SCREEN_WIDTH//2-text_surface.get_rect().width//2,SCREEN_HEIGHT//2-text_surface.get_rect().height//2))
    # Check if the menu state is "main"
    if quit_button.draw(screen):
        pygame.quit()
        exit()
        
    pygame.display.update()