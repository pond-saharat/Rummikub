import pygame
import card as c
from config import *

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class GameButton(pygame.sprite.Sprite):
	def __init__(self, rect, text,size=36):
		super().__init__()
		self.x = rect[0]
		self.y = rect[1]
		self.width = rect[2]
		self.height = rect[3]
		self.font = pygame.font.SysFont(None, 36)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.size = size
		self.text = text
		self.text = self.font.render(self.text, True, 0)
		self.text_rect = self.text.get_rect(center=(self.rect.x + (self.width//2), self.rect.y + (self.height//2)))
		self.radius = 15
		self.clicked = False
		self.hover = False
		self.visible = False
		
	def draw(self, screen):

		shadow = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
		shadow_rect = shadow.get_rect()
		pygame.draw.rect(shadow,(16, 38, 59, 100),shadow_rect, border_radius=self.radius)

		offset = 3
		shadow_rect.x = self.rect.x + offset
		shadow_rect.y = self.rect.y + offset

		screen.blit(shadow, (shadow_rect.x, shadow_rect.y))
		if not self.clicked:
			pygame.draw.rect(screen, (250, 246, 239), self.rect, border_radius=self.radius)
		else:
			pygame.draw.rect(screen, (200, 194, 189), self.rect, border_radius=self.radius)
		
		screen.blit(self.text, self.text_rect)

	def left_click_action(self, game_ui):
		self.clicked = True
		pass

class DrawButton(GameButton):
	def __init__(self, rect, text,size=36):
		super().__init__(rect,text,size)
		self.cards = []

	def left_click_action(self, game_ui):
		self.clicked = True
		deck = game_ui.game_engine.deck.deck
		region = game_ui.draw_region
		card1, card2 = tuple(deck[:2])
		card1.visible = True
		card2.visible = True
		self.cards = [card1,card2]
		card1.rect.x, card1.rect.y = region.x + GAP, region.y + GAP
		card2.rect.x, card2.rect.y = region.x + GAP + CARD_WIDTH + GAP, region.y + GAP
	
	def reset(self):
		for card in self.cards:
			card.visible = False
		self.cards = []
		
class EndTurnButton(GameButton):
	def __init__(self, rect, text,size=36):
		super().__init__(rect,text,size)
	
	def left_click_action(self, game_ui):
		self.clicked = True
		game_ui.reset_drag_parameters()
		game_ui.game_engine.next_turn()
		print(f"It's now {game_ui.game_engine.current_player}'s turn")

class FlipAllCardsButton(GameButton):
	def __init__(self, rect, text,size=36):
		super().__init__(rect,text,size)
	
	def left_click_action(self, game_ui):
		self.clicked = True
		for player in [p for p in game_ui.game_engine.players if p != game_ui.game_engine.current_player]:
			c.Card.flip_all_cards(player.hands)

class PlayForMeButton(GameButton):
	def __init__(self, rect, text,size=36):
		super().__init__(rect,text,size)
	
	def left_click_action(self, game_ui):
		self.clicked = True
		game_ui.game_engine.current_player.make_first_move(game_ui)