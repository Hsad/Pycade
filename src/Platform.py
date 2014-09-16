import pygame

class Platform(object):
	
	def __init__(self,filePath,xpos,ypos, ):
		self.image = pygame.image.load(filePath).convert_alpha()	
		self.rect= self.image.get_rect()
		self.onPlatform = False
		
		self.rect.x = xpos
		self.rect.y = ypos

	def draw(self, screen):
		screen.blit(self.image, self.rect)
