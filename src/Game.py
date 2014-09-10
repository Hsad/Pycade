import pygame, sys, Player, Platform, Knight

class Game(object):
	def __init__(self):
		pygame.init()
		self.over = False
		self.screen = pygame.display.set_mode((800,600))
		self.screen_rect = self.screen.get_rect()
		self.player = Player.Player(self.screen)

		self.knightList = []
		for x in range(5):
			KN = Knight.Knight(self.screen, x*20, 0)
			self.knightList.append(KN)

		self.clock = pygame.time.Clock()
		self.testPlatform = Platform.Platform("../assets/art/platformPlaceholder.png",500,500)
		self.timer = pygame.time.get_ticks()
		self.dt = 0
		pygame.display.set_caption("A Team Won Game ")
		self.backgroundImage = pygame.image.load("../assets/Art/BackgroundPlaceholder.jpg").convert_alpha()
		self.backgroundRect = self.backgroundImage.get_rect()


		"""apply the offset for 
				  x y"""
		offset = [0,0]


		#self.elapsed = 0


	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					self.over = True
					sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.over = True
				if event.key == pygame.K_w:
					self.player.movement[0] = True
				if event.key == pygame.K_s:
					self.player.movement[1] = True
				if event.key == pygame.K_a:
					self.player.movement[2] = True
				if event.key == pygame.K_d:
					self.player.movement[3] = True
				if event.key == pygame.K_SPACE:
					if not (self.player.jumping or self.player.ducking):
						self.player.start_jump = True


				#if both directions are pressed
				"""if self.player.movement[2] and self.player.movement[3]:
					self.player.movement[2] = False
					self.player.movement[3] = False"""

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					self.player.movement[0] = False
				if event.key == pygame.K_s:
					self.player.movement[1] = False
				if event.key == pygame.K_a:
					self.player.movement[2] = False
				if event.key == pygame.K_d:
					self.player.movement[3] = False

	def checkCollisions(self, entity):
		if entity.rect.colliderect(self.testPlatform.rect) and self.player.jumping :
			if entity.rect.bottom > self.testPlatform.rect.top and self.player.yvel>0:
				print "Hit Something!"

				if  entity.rect.left < self.testPlatform.rect.right and entity.rect.right > self.testPlatform.rect.left:
					self.player.jumping = False
					entity.rect.bottom = self.testPlatform.rect.top
					self.testPlatform.onPlatform = True
						
		if (entity.rect.left > self.testPlatform.rect.right or entity.rect.right < self.testPlatform.rect.left) and self.testPlatform.onPlatform :
		 	self.player.jumping=True
		 	self.testPlatform.onPlatform = False



	def update(self):
		self.player.update(self.dt, self.screen_rect)

		for kUp in self.knightList:
			kUp.update(self.dt, self.screen_rect, self.player)
		
		self.checkCollisions(self.player)

	def draw(self):
		#self.screen.fill((0,0,0))
		self.screen.blit(self.backgroundImage,self.screen_rect)
		#pygame.draw.line(self.screen,(0,0,0),(0,0),(300,300))
		self.testPlatform.draw(self.screen)
		self.player.draw(self.screen)

		for kDraw in self.knightList:
			kDraw.draw(self.screen)

