import pygame

class Player(object):
	def __init__(self, screen):
		self.xpos = 0
		self.ypos = screen.get_rect().height
		self.image = pygame.image.load("../assets/PlayerPlaceholder.jpg").convert_alpha()
		self.player_rect = self.image.get_rect()
		self.player_rect.x = self.xpos
		self.player_rect.y = self.ypos - self.player_rect.height

	def update(self):
		pass

	def draw(self,screen):
		pass
		screen.blit(self.image,self.player_rect)
		