import pygame, math

class Camera(object):
	def __init__(self, screen_width, screen_height):
		"""takes dimensions of window as third and fourth arguments"""
		self.rect = pygame.Rect(0,0,screen_width, screen_height)

	def update(self, player, screen):
		"""takes rect of screen as third argument,
		updates camera position"""
		self.rect.centerx = player.rect.centerx
		self.rect.centery = player.rect.centery

		#snap to sides

		if self.rect.bottom > screen.height:
			self.rect.bottom = screen.height
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > screen.width:
			self.rect.right = screen.width
		if self.rect.top < 0:
			self.rect.top = 0

	def apply_offset(self):
		offsetx = -self.rect.left
		offsety = self.rect.bottom
		return (offsetx, offsety)

