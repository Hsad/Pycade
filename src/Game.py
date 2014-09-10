import pygame, sys, Player, Platform, Knight, Ladder

class Game(object):
	def __init__(self):
		pygame.init()
		self.over = False
		self.screen = pygame.display.set_mode((800,600))
		self.screen_rect = self.screen.get_rect()
		self.player = Player.Player(self.screen)
		self.testKnight = Knight.Knight(self.screen, 0, 0)
		self.clock = pygame.time.Clock();
<<<<<<< Updated upstream
<<<<<<< Updated upstream
		self.testPlatform = Platform.Platform("../assets/art/platformPlaceholder.png",300,300)
		self.testLadder = Ladder.Ladder("../assets/art/Ladder Placeholder.png",300,300)
		self.testLadder2 = Ladder.Ladder("../assets/art/Ladder Placeholder.png",400,200)

		self.ladderList = [self.testLadder,self.testLadder2]
		
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
		self.timer = pygame.time.get_ticks()
		self.dt = 0
		pygame.display.set_caption("A Team Won Game ")
		self.backgroundImage = pygame.image.load("../assets/Art/BackgroundPlaceholder.jpg").convert_alpha()
		self.backgroundRect = self.backgroundImage.get_rect()


		"""apply the offset for 
				  x y"""
		offset = [0,0]


		#self.elapsed = 0



		#Generate a list of rects from a text file named Platform.txt
		#Type - where there isn't a platform
		#Type P where there's a standard platform
		self.platform_list_file = open("Platforms.txt", "r")
		self.platform_list = []
		self.platformx = 0
		self.platformy = 0
		
		for self.line in self.platform_list_file:
			self.platformx = 0
			self.platform_list_file_line = []
			self.platform_list_file_line = self.line.strip()
			self.platform_list_file_line = self.line.split()
			for self.symbol in self.platform_list_file_line:
				if self.symbol == "P":
					self.platform_rect = Platform.Platform("../assets/art/platformPlaceholder.png",self.platformx,self.platformy)
					self.platform_list.append(self.platform_rect)
				self.platformx += 40
			self.platformy += 40

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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
		for ladder in self.ladderList:
			if entity.rect.colliderect(ladder.rect):
				if entity.rect.centerx > ladder.rect.left and entity.rect.centerx < ladder.rect.right:
					ladder.onLadder = True
					print ladder.onLadder
					if entity.movement[0]and ladder.onLadder:
						entity.rect.centerx = ladder.rect.centerx
						entity.jumping = False
						entity.rect.y -= 10
						if entity.rect.bottom< ladder.rect.top:
							entity.rect.bottom = ladder.rect.top
					if entity.movement[1]and ladder.onLadder:
						entity.rect.centerx = ladder.rect.centerx
						entity.jumping = False
						entity.ducking = False
						entity.rect.y += 10
						

			if (entity.rect.left > ladder.rect.right or entity.rect.right < ladder.rect.left) and ladder.onLadder :
		 		self.player.jumping=True
		 		ladder.onLadder = False			





		if entity.rect.colliderect(self.testPlatform.rect) and self.player.jumping :
			if entity.rect.bottom > self.testPlatform.rect.top and self.player.yvel>0:
				

				if  entity.rect.left < self.testPlatform.rect.right and entity.rect.right > self.testPlatform.rect.left:
					self.player.jumping = False
					entity.rect.bottom = self.testPlatform.rect.top
					self.testPlatform.onPlatform = True
=======
=======
>>>>>>> Stashed changes
		for platform in self.platform_list:
			if entity.rect.colliderect(platform) and self.player.jumping:
				if entity.rect.bottom > platform.rect.top and self.player.yvel>0:
					print "Hit Something!"

					if  entity.rect.left < platform.rect.right and entity.rect.right > platform.rect.left:
						self.player.jumping = False
						entity.rect.bottom = platform.rect.top
						platform.onPlatform = True
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
						
			if (entity.rect.left > platform.rect.right or entity.rect.right < platform.rect.left) and platform.onPlatform :
				self.player.jumping=True
				platform.onPlatform = False



	def update(self):
		self.player.update(self.dt, self.screen_rect)
		self.testKnight.update(self.dt, self.screen_rect, self.player)
		
		self.checkCollisions(self.player)

	def draw(self):
		#self.screen.fill((0,0,0))
		self.screen.blit(self.backgroundImage,self.screen_rect)
		#pygame.draw.line(self.screen,(0,0,0),(0,0),(300,300))
<<<<<<< Updated upstream
<<<<<<< Updated upstream
		for ladder in self.ladderList:
			ladder.draw(self.screen)
		self.testPlatform.draw(self.screen)
=======
=======
>>>>>>> Stashed changes
		
		for platform in self.platform_list:
			platform.draw(self.screen)
		
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
		self.player.draw(self.screen)
		self.testKnight.draw(self.screen)
		

