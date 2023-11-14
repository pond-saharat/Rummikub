# import pygame
# import random

# # 初始化pygame
# pygame.init()

# # 设置屏幕尺寸
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# # 设置标题
# pygame.display.set_caption("Rummikub Card Game")

# # 定义颜色
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # 卡牌类
# class Card:
#     def __init__(self, number, color):
#         self.number = number
#         self.color = color

#     def display(self, screen, x, y):
#         # 这里应该有卡牌的显示逻辑，例如使用pygame来绘制卡牌
#         pygame.draw.rect(screen, self.color, (x, y, 50, 70))
#         font = pygame.font.SysFont(None, 24)
#         text = font.render(str(self.number), True, BLACK)
#         screen.blit(text, (x + 20, y + 25))

# # 游戏主循环
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # 游戏逻辑放这里

#     # 清屏
#     screen.fill(WHITE)

#     # 绘制卡牌示例
#     card = Card(random.randint(1, 10), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
#     card.display(screen, 100, 100)

#     # 更新屏幕
#     pygame.display.flip()

# # 退出游戏
# pygame.quit()



import pygame,sys
import game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600),flags=pygame.SHOWN)  # Set the screen size
    pygame.display.set_caption("Rummikub Game")
    
    game_instance = game.Game(screen)
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_instance.update()
        game_instance.render()

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
