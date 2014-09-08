import pygame

class Player(object):
	def __init__(self, screen):
		#left == 0, right == 1;
		self.direction = 0;
		self.xpos = 0
		self.ypos = screen.get_rect().height
		self.image = pygame.image.load("../assets/Art/PlayerPlaceholder.png").convert_alpha()
		#self.image = pygame.image.load("../assets/Art/princess_run.png").convert_alpha()
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

		#values for sprite changes
		"""self.framerate = 4
		self.framebuffer = 0
		self.timer = pygame.time.get_ticks()
		self.elapsed = 0"""

	def update(self, dt, screen_rect):
		"""self.elapsed = pygame.time.get_ticks() - self.timer"""
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
			"""self.direction = 1;"""
			if self.xvel < -self.xmax:
				self.xvel = -self.xmax
		if self.movement[3] and not self.ducking:
			self.xvel += self.xaccel*dt
			"""self.direction = 0;"""
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


		#sprite changing
		"""if self.movement == [False, False, False, False]:
			self.frame = 0
		else:
			self.framebuffer += self.elapsed
			if self.framebuffer > 1000.0/self.framerate:
				self.framebuffer = 0
				self.frame += 1
			if self.frame > 3:
				self.frame = 0"""


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
			""",pygame.Rect(64*(self.frame), self.direction*80, 64, 80))"""
			screen.blit(self.image, self.rect) 
		