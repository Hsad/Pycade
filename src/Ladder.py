import pygame

class Ladder(object):
	
	def __init__(self,filePath,xpos,ypos, ):
		self.image = pygame.image.load(filePath).convert_alpha()	
		self.rect= self.image.get_rect()
		self.onLadder = False
		
		self.rect.x = xpos
		self.rect.y = ypos


	def update(self):
		pass

	def draw(self, screen):
		screen.blit(self.image, self.rect)
