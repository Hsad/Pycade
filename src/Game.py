import pygame, sys, Player, Platform, Knight, Ladder

class Game(object):
	def __init__(self):
		pygame.init()
		self.over = False
		self.screen = pygame.display.set_mode((800,600))
		self.screen_rect = self.screen.get_rect()
		self.player = Player.Player(self.screen)
		#initilizing Knight Array
		self.knightList = []
		"""for x in range(5):
			KN = Knight.Knight(self.screen, x*20, 0)
			self.knightList.append(KN)"""

		self.clock = pygame.time.Clock()
		self.ladderList = []
		self.timer = pygame.time.get_ticks()
		self.dt = 0
		pygame.display.set_caption("Royal Rescue")
		self.backgroundImage = pygame.image.load("../assets/Art/background.png").convert_alpha()
		self.backgroundRect = self.backgroundImage.get_rect()
		self.dirt_image = pygame.image.load("../assets/Art/Ground_Placeholder.png").convert_alpha()


		"""apply the offset for x y"""
		offset = [0,0]


		#self.elapsed = 0



		#Generate a list of rects from a text file named Platform.txt
		#Type - where there isn't a platform
		#Type P where there's a standard platform
		self.platform_file = open("Platforms.txt", "r")
		self.platform_boundaries_list = []
		self.platform_draw_list = []
		self.platformx = 0
		self.platformy = 0
		self.previous_tile_is_platform = False
		
		#Parse the text file
		for self.line in self.platform_file:
			self.platformx = 0
			self.platform_file_line = []
			self.platform_file_line = self.line.strip()
			self.platform_file_line = self.line.split()
			for self.symbol in self.platform_file_line:
				if self.symbol == "P":
					if self.previous_tile_is_platform:
						self.platform_boundaries_list[-1].rect.width += 40
						self.platform_draw_list.append(Platform.Platform("../assets/art/platform_middle_col.png",self.platformx,self.platformy))
					else:
						self.platform_boundaries_list.append(Platform.Platform("../assets/art/platform_begin_col.png",self.platformx,self.platformy))
						self.platform_boundaries_list[-1].rect.height = 15
						self.platform_boundaries_list[-1].rect.top = self.platformy
						self.platform_draw_list.append(Platform.Platform("../assets/art/platform_begin_col.png",self.platformx,self.platformy))
						self.previous_tile_is_platform = True
				elif self.symbol == "L":
					if self.previous_tile_is_platform:


						self.platform_boundaries_list[-1].rect.width += 40
					self.ladderList.append(Ladder.Ladder("../assets/art/ladder_col.png", self.platformx, self.platformy))
				else:
					if self.previous_tile_is_platform and len(self.platform_draw_list) > 0:
						self.platform_draw_list[-1].image = pygame.image.load("../assets/art/platform_end_col.png").convert_alpha()
					self.previous_tile_is_platform = False
				if self.symbol == "S":
					self.player.rect.x = self.platformx
					self.player.rect.y = self.platformy
				if self.symbol == "K":
					self.knightList.append(Knight.Knight(self.screen, self.platformx, self.platformy))
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
		if entity == self.player:

			for ladder in self.ladderList:
				if entity.rect.colliderect(ladder.rect):
					print  str(entity.onLadder) + " " +  str(entity.movement[1])

					entity.currentLadder = ladder
					if entity.rect.centerx > entity.currentLadder.rect.left and entity.rect.centerx < entity.currentLadder.rect.right and entity.movement[0]:
						entity.onLadder = True

						if entity.onLadder:
							entity.rect.centerx = entity.currentLadder.rect.centerx
							entity.jumping = False
							entity.rect.y -= 10 *self.dt
							if entity.rect.bottom< entity.currentLadder.rect.top:
								entity.rect.bottom = entity.currentLadder.rect.top
						if entity.onLadder and entity.movement[1]:
							entity.rect.y += 10 *self.dt

					#	entity.rect.centerx = entity.currentLadder.rect.centerx
					#	entity.jumping = False
					#	entity.ducking = False
					#	entity.yvel += 10 * self.dt


				if entity.currentLadder and (entity.rect.left > entity.currentLadder.rect.right or entity.rect.right < entity.currentLadder.rect.left) and entity.onLadder :

					entity.jumping=True
		 			entity.onLadder = False
		 			entity.currentLadder = None

			for platform in self.platform_boundaries_list:			
				if entity.rect.colliderect(platform) and entity.jumping: 
					entity.currentPlatform = platform;
					if entity.rect.bottom > entity.currentPlatform.rect.top and self.player.yvel>0:
						if  entity.rect.left < entity.currentPlatform.rect.right and entity.rect.right > entity.currentPlatform.rect.left and entity.rect.bottom > entity.currentPlatform.rect.top and entity.rect.top < entity.currentPlatform.rect.bottom and entity.platform_rect.top < entity.currentPlatform.rect.top: 
							entity.jumping = False
							entity.rect.bottom = entity.currentPlatform.rect.top
							entity.onPlatform = True
							break;
						if (entity.rect.left > entity.currentPlatform.rect.right or entity.rect.right < entity.currentPlatform.rect.left):
							entity.onPlatform = False
				if entity.currentPlatform and (entity.rect.left > entity.currentPlatform.rect.right or entity.rect.right < entity.currentPlatform.rect.left or entity.rect.top > entity.currentPlatform.rect.bottom or entity.rect.bottom < entity.currentPlatform.rect.top) and entity.onPlatform:
					entity.jumping=True
					entity.currentPlatform = None
					#entity.onPlatform = False
	



	def update(self):
		self.player.update(self.dt, self.screen_rect)		
		#Moves the tiles to give the illusion of player movement
		if self.player.camerax + self.player.movement_amount >= 0 and self.player.camerax <= self.player.maxx:
			self.player.camerax += self.player.movement_amount
			for ladder in self.ladderList:
				ladder.rect.x -= self.player.movement_amount
			for platform in self.platform_boundaries_list:
				platform.rect.x -= self.player.movement_amount
			for platform in self.platform_draw_list:
				platform.rect.x -= self.player.movement_amount
			for knight in self.knightList:
				knight.rect.x -= self.player.movement_amount
		elif self.player.camerax + self.player.movement_amount < 0:
			for ladder in self.ladderList:
				ladder.rect.x -= self.player.camerax
			for platform in self.platform_boundaries_list:
				platform.rect.x -= self.player.camerax
			for platform in self.platform_draw_list:
				platform.rect.x -= self.player.camerax
			for knight in self.knightList:
				knight.rect.x -= self.player.camerax
			self.player.camerax = 0

		#knights
		for kUp in self.knightList:
			kUp.update(self.dt, self.screen_rect, self.player, self.knightList, self.platform_boundaries_list, self.ladderList)
		
		self.checkCollisions(self.player)

	def draw(self):
		#self.screen.fill((0,0,0))
		self.screen.blit(self.backgroundImage,self.screen_rect)
		#pygame.draw.line(self.screen,(0,0,0),(0,0),(300,300))
		for ladder in self.ladderList:
			ladder.draw(self.screen)
		for platform in self.platform_draw_list:
			dirty = platform.rect.y + 20
			while dirty <= self.screen.get_rect().width:
				self.screen.blit (self.dirt_image, pygame.Rect(platform.rect.x, dirty, 40, 40))
				dirty += 40
			platform.draw(self.screen)
		self.player.draw(self.screen)
		#knights
		for kDraw in self.knightList:
			kDraw.draw(self.screen)
