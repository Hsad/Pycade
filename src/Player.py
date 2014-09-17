import pygame	

class Player(object):
	def __init__(self, screen):
		self.screen = screen
		
		#left == 1, right == 0
		self.direction = 0

		"""State:
			0 = running
			1 = idle
			2 = skidding
			3 = jumping
			4 = ducking
			5 = climbing
		"""
		self.state = 0

		#images
		#self.image = pygame.image.load("../assets/Art/PlayerPlaceholder.png").convert_alpha()
		self.image = pygame.image.load("../assets/Art/princess_master.png").convert_alpha()
		self.duck_image = pygame.image.load("../assets/Art/PlayerDuckingPlaceholder.png").convert_alpha()
		
		#rects
		self.duck_rect = self.duck_image.get_rect()
		self.rect = pygame.Rect(0,0,64,80)
		self.platform_rect = pygame.Rect(0,0,44,15)

		self.future_rect = self.rect
		self.future_rect.width = 45 #Feels better if we don't check all the way to the end for collisions
		self.future_rect.x += 10

		self.movement_amount = 0
		self.camerax = 0
		self.maxx = 4000 #The width of the level


		self.rect.x = 0
		self.rect.y = screen.get_rect().height
		#up, down, left, right
		self.movement = [False for i in range(4)]
		self.xvel = 0
		self.yvel = 0

		#have they commenced the jump?
		self.start_jump = False

		#they are in the air
		self.jumping = True

		#direction of player, facing right
		#some player states
		self.ducking = False
		self.onLadder= False
		self.onPlatform = True #We start her on a platform, so this has to start true if we want her to be able to fall off
		self.currentPlatform = None
		self.currentLadder = None

		#acceleration and deceleration

		self.xaccel = 3000
		self.gravity = 2000
		self.xdecel = 2000
		self.onPlatform = False

		#max horizontal speed
		self.xmax = 300

		#values for sprite changes
		self.frame = 0
		self.framerate = 4
		self.framebuffer = 0
		self.framelength = 4

	def update(self, dt, screen_rect):
		self.future_rect = self.rect.move(0,0)
		self.platform_rect.bottom = self.rect.bottom
		self.platform_rect.left = self.rect.left

		if self.movement[0]:
			pass


		if self.movement[1]:
			if not self.onLadder:
				self.ducking = True
				self.duck_rect.left = self.rect.left
				self.duck_rect.bottom = self.rect.bottom
				self.xvel = 0
				self.state = 4
				self.framelength = 1
			else:
				self.rect.x += 10 * dt
	
		else:
			self.ducking=False
			self.duck_rect.left = self.rect.left
			self.duck_rect.bottom = self.rect.bottom

		#accelerate

		#left
		if self.movement[2] and not self.ducking:
			self.direction = 1
			if self.xvel > 0:
				self.xvel -= self.xdecel*dt
				self.state = 2
				self.framelength = 2
			else:
				self.xvel -= self.xaccel*dt
				self.framelength = 4
				self.state = 0
			if self.xvel < -self.xmax:
				self.xvel = -self.xmax

		#right
		if self.movement[3] and not self.ducking:
			self.direction = 0
			if self.xvel < 0:
				self.xvel += self.xdecel*dt
				self.state = 2
				self.framelength = 2
			else:
				self.xvel += self.xaccel*dt
				self.framelength = 4
				self.state = 0
			if self.xvel > self.xmax:
				self.xvel = self.xmax

		if self.movement[2] == self.movement[3] and not self.ducking:
			self.deceleration("x", dt)
			self.state = 1
			self.framelength = 4


		if self.start_jump:
			self.jumping = True
			self.yvel = -600
			self.start_jump = False

		if self.jumping:
			self.yvel += self.gravity*dt
			self.state = 3
			self.framelength = 1
		else:
			self.yvel = 0

		if self.onLadder:
			self.state = 5
			self.framelength = 2

		self.future_rect.x += self.xvel*dt
		self.future_rect.y += self.yvel*dt




		#boundary checking
		if self.future_rect.right > screen_rect.right:
			self.future_rect.right = screen_rect.right
			self.xvel = 0
		if self.future_rect.left < 0:
			self.future_rect.left = 0
			self.xvel = 0
		if self.future_rect.bottom > screen_rect.bottom:
			self.future_rect.bottom = screen_rect.bottom
			self.jumping = False

		#Make the player "move" based on their inputs
		self.movement_amount = self.future_rect.x - self.rect.x
		if self.camerax + self.movement_amount >= 0 and self.camerax + self.movement_amount <= self.maxx:
			if self.direction == 1: #If we're moving left, the player stops 100 pixels to the left of the middle of the screen
				if self.rect.x >= self.screen.get_rect().width/2-100:
					self.rect = self.future_rect
			if self.direction == 0: #If we're moving right the player stops 100 pixels to the right of the middle of the screen
				if self.rect.x <= self.screen.get_rect().width/2+100:
					self.rect = self.future_rect
			if self.jumping:
				self.rect.y = self.future_rect.y
		else:
			self.rect = self.future_rect



		#sprite changing
		if not (self.onLadder and not self.movement[0]):
			self.framebuffer += dt
			if self.framebuffer > .5/self.framerate:
				self.framebuffer = 0
				self.frame += 1
		if self.frame >= self.framelength:
			self.frame = 0


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
		if self.onLadder:
			screen.blit(self.image, self.rect, pygame.Rect(64*(self.frame), (2*self.state) * 80 , 64, 80))
		if self.jumping:
			if self.yvel < 0:
				screen.blit(self.image, self.rect, pygame.Rect(0, (2*self.state + self.direction) * 80 , 64, 80)) 
			if self.yvel > 0:
				screen.blit(self.image, self.rect, pygame.Rect(64, (2*self.state + self.direction) * 80 , 64, 80)) 
		else:
			screen.blit(self.image, self.rect, pygame.Rect(64*(self.frame), (2*self.state + self.direction) * 80 , 64, 80))