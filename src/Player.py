import pygame

class Player(object):
	def __init__(self, screen):
		self.xpos = 0
		self.ypos = screen.get_rect().height
		self.image = pygame.image.load("../assets/Art/PlayerPlaceholder.png").convert_alpha()
		self.duck_image = pygame.image.load("../assets/Art/PlayerDuckingPlaceholder.png").convert_alpha()
		self.duck_rect = self.duck_image.get_rect()
		self.rect = self.image.get_rect()
		self.rect.x = self.xpos
		self.rect.y = self.ypos - self.rect.height

		#up, down, left, right
		self.movement = [False for i in range(4)]
		self.xvel = 0
		self.yvel = 0

		#have they commenced the jump?
		self.start_jump = False

		#they are in the air
		self.jumping = False

		self.ducking = False

		#acceleration and deceleration
		self.xaccel = 8000
		self.gravity = 5000
		self.xdecel = 8000

		#max horizontal speed
		self.xmax = 10000

	def update(self, dt, screen_rect):
		future_rect = self.rect.move(0,0)

		"""if self.movement[0]:
			future_rect.y -= self.yvel*dt
		if self.movement[1]:
			future_rect.y += self.yvel*dt"""

		if self.movement[1]:
			self.ducking = True
			self.duck_rect.left = self.rect.left
			self.duck_rect.bottom = self.rect.bottom
			self.xvel = 0
			

		else:
			self.ducking=False
			self.duck_rect.left = self.rect.left
			self.duck_rect.bottom = self.rect.bottom

		#accelerate
		if self.movement[2] and not self.ducking:
			self.xvel -= self.xaccel*dt
			if self.xvel < -self.xmax:
				self.xvel = -self.xmax
		if self.movement[3] and not self.ducking:
			self.xvel += self.xaccel*dt
			if self.xvel > self.xmax:
				self.xvel = self.xmax

		if self.movement[2] == self.movement[3]:
			self.deceleration("x", dt)


		if self.start_jump:
			self.jumping = True
			self.yvel = -1500
			self.start_jump = False

		if self.jumping:
			self.yvel += self.gravity*dt
		else:
			self.yvel = 0

		future_rect.x += self.xvel*dt
		future_rect.y += self.yvel*dt


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
			self.jumping = False
		self.rect = future_rect


		print self.xvel

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
		if self.ducking:
			screen.blit(self.duck_image,self.duck_rect)
		else:
			screen.blit(self.image,self.rect)
		