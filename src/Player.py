import pygame

class Player(object):
	def __init__(self, screen):
		self.xpos = 0
		self.ypos = screen.get_rect().height
		self.image = pygame.image.load("../assets/PlayerPlaceholder.png").convert_alpha()
		self.duck_image = pygame.image.load("../assets/PlayerDuckingPLaceholder.png").convert_alpha()
		self.duck_rect = self.duck_image.get_rect()
		self.rect = self.image.get_rect()

		self.rect.x = self.xpos
		self.rect.y = self.ypos - self.rect.height
		self.movement = [False for i in range(4)]
		self.xvel = 0
		self.yvel = 0
		self.duck = False
		#acceleration and deceleration
		self.xaccel = 8000
		self.yaccel = 5000
		self.xdecel = 8000

		self.xmax = 10000

	def update(self, dt, screen_rect):
		future_rect = self.rect.move(0,0)

		"""if self.movement[0]:
			future_rect.y -= self.yvel*dt
		if self.movement[1]:
			future_rect.y += self.yvel*dt"""

		#ducking


		if self.movement[1]:
			self.duck = True
			self.duck_rect.left = self.rect.left
			self.duck_rect.bottom = self.rect.bottom
			self.xvel =self.yvel= self.xaccel=self.yaccel= 0
			

		else:
			self.duck=False
			self.duck_rect.left = self.rect.left
			self.duck_rect.bottom = self.rect.bottom
			self.xaccel = 8000
			self.yaccel = 5000

			
		#accelerate
		if self.movement[2]:
			self.xvel -= self.xaccel*dt
			if self.xvel < -self.xmax:
				self.xvel = -self.xmax
		if self.movement[3]:
			self.xvel += self.xaccel*dt
			if self.xvel > self.xmax:
				self.xvel = self.xmax 

		if self.movement[2] == self.movement[3]:
			self.deceleration("x", dt)

		future_rect.x += self.xvel*dt


		#boundary checking
		if future_rect.right > screen_rect.right:
			future_rect.right = screen_rect.right
			self.xvel = 0
		if future_rect.left < 0:
			future_rect.left = 0
			self.xvel = 0
		if future_rect.top < 0:
			future_rect.top = 0
		if future_rect.bottom > screen_rect.bottom:
			future_rect.bottom = screen_rect.bottom

		self.rect = future_rect

	def deceleration(self, dimension, dt):
		if dimension == "x":
			if self.xvel < 0:
				self.xvel += self.xdecel*dt
				if self.xvel > 0:
					self.xvel = 0
			if self.xvel > 0:
				self.xvel -= self.xdecel*dt
				if self.xvel < 0:
					self.xvel = 0



	def draw(self,screen):
		if self.duck:
			screen.blit(self.duck_image,self.duck_rect)
		else:
			screen.blit(self.image,self.rect)
		