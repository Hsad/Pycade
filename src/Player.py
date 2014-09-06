import pygame

class Player(object):
	def __init__(self, screen):
		self.xpos = 0
		self.ypos = screen.get_rect().height
		self.image = pygame.image.load("../assets/PlayerPlaceholder.jpg").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = self.xpos
		self.rect.y = self.ypos - self.rect.height
		self.movement = [False for i in range(4)]
		self.xvel = 0
		self.yvel = 0

		#acceleration and deceleration
		self.xaccel = 4000
		self.yaccel = 4000
		self.xdecel = 10000

		self.xmax = 4000

	def update(self, dt, screen_rect):
		future_rect = self.rect.move(0,0)

		"""if self.movement[0]:
			future_rect.y -= self.yvel*dt
		if self.movement[1]:
			future_rect.y += self.yvel*dt"""


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

		print self.xvel


		#boundary checking
		if future_rect.right > screen_rect.right:
			future_rect.right = screen_rect.right
		if future_rect.left < 0:
			future_rect.left = 0
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
		screen.blit(self.image,self.rect)
		