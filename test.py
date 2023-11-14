# import pygame
# import random

# pygame.init()
# clock = pygame.time.Clock()

# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 1000
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# pygame.display.set_caption("Rummikub Game")

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (200, 200, 200)
# COLORS = {
#     'Red': (255, 0, 0),
#     'Blue': (0, 0, 255),
#     'Green': (0, 255, 0),
#     'Yellow': (255, 255, 0)
# }

# # Card 类
# class Card:
#     def __init__(self, color, number):
#         self.color = color
#         self.number = number
#         self.rect = pygame.Rect(0, 0, 50, 80)  # 初始化卡片的矩形区域

#     def set_position(self, x, y):
#         self.rect.x = x
#         self.rect.y = y

#     def draw(self, screen):
#         card_color = COLORS.get(self.color, BLACK)  # 获取卡片的颜色
#         pygame.draw.rect(screen, card_color, self.rect)
#         font = pygame.font.Font(None, 36)
#         text = font.render(f"{self.number}", True, BLACK)
#         text_rect = text.get_rect(center=self.rect.center)
#         screen.blit(text, text_rect)
    
#     def move_up(self, offset):
#         self.rect.y -= offset

#     def reset_position(self, original_y):
#         self.rect.y = original_y

# # RummikubGame 类
# class RummikubGame:
#     def __init__(self):
#         self.tile_deck = self.create_tile_deck()
#         self.players_hands = [[], [], [], []]
#         self.selected_cards = set()  # 使用集合来避免重复
#         self.original_card_positions = {}  # 存储牌的原始位置

#     def create_tile_deck(self):
#         colors = ['Red', 'Blue', 'Green', 'Yellow']
#         tiles = [Card(color, number) for color in colors for number in range(1, 14)] * 2
#         random.shuffle(tiles)
#         return tiles

#     # 多人
#     def deal_tiles(self, num=14):
#         for hand in self.players_hands:
#             for _ in range(num):
#                 hand.append(self.tile_deck.pop())
#         self.update_all_hands_positions()
#         for hand in self.players_hands:
#             for card in self.players_hands[0]:
#                 self.original_card_positions[card] = card.rect.y
        

#     def update_all_hands_positions(self):
#         screen_positions = [
#             (10, SCREEN_HEIGHT - 80),  # 底部
#             (SCREEN_WIDTH - 60, 0),   # 右边
#             (10, 10),                  # 顶部
#             (10, 0)   # 左边
#         ]
#         for i, hand in enumerate(self.players_hands):
#             self.set_hand_position(hand, *screen_positions[i])

#     def set_hand_position(self, hand, x_start, y_start):
#         for j, card in enumerate(hand):
#             if y_start in [10, SCREEN_HEIGHT - 80]:  # 顶部或底部
#                 x = x_start + j * 60
#                 y = y_start
#             else:  # 左边或右边
#                 x = x_start
#                 y = y_start + j * 80
#             card.set_position(x, y)
            
#     # 排序 
#     def sort_player_hand(self, player_index):
#         self.players_hands[player_index].sort(key=lambda card: (card.number, card.color))
#         self.update_hand_positions(player_index)
#     # 更新手牌的位置
#     def update_hand_positions(self, player_index):
#         for i, card in enumerate(self.players_hands[player_index]):
#             card.set_position(10 + i * 60, SCREEN_HEIGHT - 80)  # 根据需要调整位置
            
    
#     def draw(self, screen):
#         for hand in self.players_hands:
#             for card in hand:
#                 card.draw(screen)

#     # 处理牌的选择与否
#     def handle_click(self, x, y):
#         for card in self.players_hands[0]:
#             if card.rect.collidepoint(x, y):
#                 if card in self.selected_cards:
#                     self.selected_cards.remove(card)  # 如果已选中，则取消选择
#                     card.reset_position(self.original_card_positions[card])
#                 else:
#                     self.selected_cards.add(card)  # 如果未选中，则添加到选中列表
#                     card.move_up(20)

#     # 实现组合逻辑
#     def combine_selected_cards(self):
#         if len(self.selected_cards) >= 3:  # 假设至少需要3张牌来组成有效组合
#             print("组合牌:", self.selected_cards)
#             # 这里可以添加更复杂的组合逻辑
            
# game = RummikubGame()
# game.deal_tiles()

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             x, y = pygame.mouse.get_pos()
#             game.handle_click(x, y)
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_c:  # 假设按下 'C' 键来确认组合
#                 game.combine_selected_cards()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_s:  # 按下 'S' 键进行排序
#                 game.sort_player_hand(0)  # 假设为第一个玩家排序手牌

#     screen.fill(WHITE)
#     game.draw(screen)
#     for card in game.selected_cards:
#         pygame.draw.rect(screen, BLACK, card.rect, 4)  # 高亮显示选中的牌
        
#     pygame.display.flip()
#     clock.tick(60)  # 控制游戏循环以每秒60帧的速度运行


# pygame.quit()


import pygame
import random

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rummikub Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
COLORS = {
    'Red': (255, 0, 0),
    'Blue': (100, 100, 255),
    'Green': (0, 255, 0),
    'Yellow': (255, 255, 0)
}

# 全局字体对象
font = pygame.font.Font(None, 36)

# Card 类
class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number
        self.rect = pygame.Rect(0, 0, 50, 70)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        card_color = COLORS.get(self.color, BLACK)
        pygame.draw.rect(screen, card_color, self.rect)
        text = font.render(f"{self.number}", True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def move_up(self, offset):
        self.rect.y -= offset

    def reset_position(self, original_y):
        self.rect.y = original_y

# RummikubGame 类
class RummikubGame:
    def __init__(self):
        self.tile_deck = self.create_tile_deck()
        self.players_hands = [[], [], [], []]
        self.selected_cards = set()
        self.original_card_positions = {}

    def create_tile_deck(self):
        colors = ['Red', 'Blue', 'Green', 'Yellow']
        tiles = [Card(color, number) for color in colors for number in range(1, 14)] * 2
        random.shuffle(tiles)
        return tiles

    def deal_tiles(self, num=14):
        for hand in self.players_hands:
            for _ in range(num):
                hand.append(self.tile_deck.pop())
        self.update_all_hands_positions()

    def update_all_hands_positions(self):
        screen_positions = [(50, SCREEN_HEIGHT - 80), (SCREEN_WIDTH - 60, 20), (10, 20), (50, 10)]
        for i, hand in enumerate(self.players_hands):
            self.set_hand_position(hand, *screen_positions[i])

    # def set_hand_position(self, hand, x_start, y_start):
    #     row_limit = 14  # 每行的牌数限制
    #     card_width = 60
    #     spacing = 30

    #     for j, card in enumerate(hand):
    #         x = x_start + (j % row_limit) * spacing if y_start in [10, SCREEN_HEIGHT - 80] else x_start
    #         y = y_start + (j // row_limit) * card_width  if y_start not in [10, SCREEN_HEIGHT - 80] else y_start
    #         card.set_position(x, y)
    #         self.original_card_positions[card] = y

    def set_hand_position(self, hand, x_start, y_start):
        for j, card in enumerate(hand):
            x = x_start + (j * 60) if y_start in [10, SCREEN_HEIGHT - 80] else x_start
            y = y_start + (j * 80) if y_start not in [10, SCREEN_HEIGHT - 80] else y_start
            card.set_position(x, y)
            self.original_card_positions[card] = y

    def draw(self, screen):
        for hand in self.players_hands:
            for card in hand:
                card.draw(screen)

    def handle_click(self, x, y):
        for card in self.players_hands[0]:
            if card.rect.collidepoint(x, y):
                if card in self.selected_cards:
                    self.selected_cards.remove(card)
                    card.reset_position(self.original_card_positions[card])
                else:
                    self.selected_cards.add(card)
                    card.move_up(20)

    def sort_player_hand(self, player_index):
        self.players_hands[player_index].sort(key=lambda card: (card.number, card.color))
        self.update_hand_positions(player_index)

    def update_hand_positions(self, player_index):
        x_start, y_start = 10, SCREEN_HEIGHT - 80
        for i, card in enumerate(self.players_hands[player_index]):
            card.set_position(x_start + i * 60, y_start)
            self.original_card_positions[card] = y_start

game = RummikubGame()
game.deal_tiles()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            game.handle_click(x, y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game.sort_player_hand(0)

    screen.fill(WHITE)
    game.draw(screen)
    for card in game.selected_cards:
        pygame.draw.rect(screen, BLACK, card.rect, 4)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
