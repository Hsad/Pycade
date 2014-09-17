import pygame, random, sys, Player, Platform, Knight, Ladder

class Game(object):
	def __init__(self):
		pygame.init()
		self.over = False
		self.screen = pygame.display.set_mode((800,600))
		self.screen_rect = self.screen.get_rect()
		self.player = Player.Player(self.screen)
		#initilizing Knight Array
		self.knightList = []

		self.clock = pygame.time.Clock()
		self.ladderList = []
		self.timer = pygame.time.get_ticks()
		self.dt = 0
		pygame.display.set_caption("Royal Rescue")
		self.backgroundImage = pygame.image.load("../assets/Art/background.png").convert_alpha()
		self.backgroundRect = self.backgroundImage.get_rect()
		
		self.grass_platform_image_begin = pygame.image.load("../assets/art/platform_begin.png").convert_alpha()
		self.grass_platform_image_middle = pygame.image.load("../assets/art/platform_middle.png").convert_alpha()
		self.grass_platform_image_end = pygame.image.load("../assets/art/platform_end.png").convert_alpha()
		self.castle_platform_image_begin = pygame.image.load("../assets/art/platform_begin_col.png").convert_alpha()
		self.castle_platform_image_middle = pygame.image.load("../assets/art/platform_middle_col.png").convert_alpha()
		self.castle_platform_image_end = pygame.image.load("../assets/art/platform_end_col.png").convert_alpha()
		
		self.dirt_image1 = pygame.image.load("../assets/Art/dirt1.png").convert_alpha()
		self.dirt_image2 = pygame.image.load("../assets/Art/dirt2.png").convert_alpha()
		self.dirt_image3 = pygame.image.load("../assets/Art/dirt3.png").convert_alpha()
		self.dirt_image4 = pygame.image.load("../assets/Art/dirt4.png").convert_alpha()
		self.dirt_type_list = []
		self.stone_image1 = pygame.image.load("../assets/Art/castle_column1.png").convert_alpha()
		self.stone_image2 = pygame.image.load("../assets/Art/castle_column2.png").convert_alpha()
		self.stone_image3 = pygame.image.load("../assets/Art/castle_column3.png").convert_alpha()
		self.stone_image4 = pygame.image.load("../assets/Art/castle_column4.png").convert_alpha()
		self.stone_type_list = []
		
		#Create a list of miscellaneous items in the level so the camera can scroll them as well
		self.set_props = []
		self.castle_entrence_image = pygame.image.load("../assets/Art/Castle_Gate.png").convert_alpha()
		self.enemy_castle_entrence_rect = self.castle_entrence_image.get_rect()
		self.good_castle_entrence_rect = self.castle_entrence_image.get_rect()
		self.good_castle_entrence_rect.x -= self.good_castle_entrence_rect.width/2
		self.set_props.append(self.enemy_castle_entrence_rect)
		self.set_props.append(self.good_castle_entrence_rect)
		self.castle_background_image = pygame.image.load("../assets/Art/Castle_Background.png").convert_alpha()
		
		#Make the player spawn above the screen just to the right of the castle
		self.player.rect.x = self.good_castle_entrence_rect.right
		self.player.rect.y = 0-self.player.rect.height

		#Generate a list of rects from a text file named Platform.txt
		#Type - where there isn't a platform
		#Type P where there's a standard platform
		self.platform_file = open("Platforms.txt", "r")
		self.platform_boundaries_list = []
		self.platform_draw_list = []
		self.platformx = 0
		self.platformy = 0
		self.previous_tile_is_platform = False
		self.previous_platform = ""
		
		#Parse the text file
		for self.line in self.platform_file:
			self.platformx = 0
			self.platform_file_line = []
			self.platform_file_line = self.line.strip()
			self.platform_file_line = self.line.split()
			self.player.maxx = len(self.line)*40-self.screen.get_rect().width #Set the right most boundary to how long a line in the text file is
			for self.symbol in self.platform_file_line:
				if self.symbol == "P":
					if self.previous_tile_is_platform:
						self.platform_boundaries_list[-1].rect.width += 40
						self.platform_draw_list.append(Platform.Platform("../assets/art/platform_middle.png",self.platformx,self.platformy))
						for i in range(self.screen.get_rect().height/40):
							self.dirt_type_list.append(random.randint(1, 4))
					else:
						self.platform_boundaries_list.append(Platform.Platform("../assets/art/platform_begin.png",self.platformx,self.platformy))
						self.platform_boundaries_list[-1].rect.height = 15
						self.platform_boundaries_list[-1].rect.top = self.platformy
						self.platform_draw_list.append(Platform.Platform("../assets/art/platform_begin.png",self.platformx,self.platformy))
						for i in range(self.screen.get_rect().height/40):
							self.dirt_type_list.append(random.randint(1, 4))
						self.previous_tile_is_platform = True
						self.previous_platform = "Grass"
						
				elif self.symbol == "C":
					if self.previous_tile_is_platform:
						self.platform_boundaries_list[-1].rect.width += 40
						self.platform_draw_list.append(Platform.Platform("../assets/art/platform_middle_col.png",self.platformx,self.platformy))
						for i in range(self.screen.get_rect().height/40):
							self.dirt_type_list.append(random.randint(1, 4))
					else:
						#Keeps track of the castle platform furthest to the left
						if self.platformx < self.enemy_castle_entrence_rect.right or self.enemy_castle_entrence_rect.x == 0:
							self.enemy_castle_entrence_rect.right = self.platformx
						self.platform_boundaries_list.append(Platform.Platform("../assets/art/platform_begin_col.png",self.platformx,self.platformy))
						self.platform_boundaries_list[-1].rect.height = 15
						self.platform_boundaries_list[-1].rect.top = self.platformy
						self.platform_draw_list.append(Platform.Platform("../assets/art/platform_begin_col.png",self.platformx,self.platformy))
						for i in range(self.screen.get_rect().height/40):
							self.dirt_type_list.append(random.randint(1, 4))
						self.previous_tile_is_platform = True
						self.previous_platform = "Castle"
				elif self.symbol == "L":
					if self.previous_tile_is_platform:


						self.platform_boundaries_list[-1].rect.width += 40
					self.ladderList.append(Ladder.Ladder("../assets/art/ladder_col.png", self.platformx, self.platformy))
				else:
					#When we end a platform block, if it was more than one tile wide, make the last tile the end sprite.
					#If the platform block was only one tile wide, make it the middle platform
					if self.previous_tile_is_platform and len(self.platform_draw_list) > 1:
						if self.platform_draw_list[-2].rect.x == self.platform_draw_list[-1].rect.x-40 and self.platform_draw_list[-2].rect.y == self.platform_draw_list[-1].rect.y:
							if self.previous_platform == "Castle":
								self.platform_draw_list[-1].image = self.castle_platform_image_end
							if self.previous_platform == "Grass":
								self.platform_draw_list[-1].image = self.grass_platform_image_end
						else:
							if self.previous_platform == "Castle":
								self.platform_draw_list[-1].image = self.castle_platform_image_middle
							if self.previous_platform == "Grass":
								self.platform_draw_list[-1].image = self.grass_platform_image_middle
					self.previous_tile_is_platform = False
				if self.symbol == "K":
					self.knightList.append(Knight.Knight(self.screen, self.platformx, self.platformy,False))
				if self.symbol == "E":
					self.knightList.append(Knight.Knight(self.screen, self.platformx, self.platformy,True))
				self.platformx += 40
			self.platformy += 40
			
		#Load the music
		self.background_music = pygame.mixer.music.load("../assets/Audio/Music/Castle.wav")
		pygame.mixer.music.play(-1, 0.0)
		
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
					entity.currentLadder = ladder
					if entity.rect.centerx > entity.currentLadder.rect.left and entity.rect.centerx < entity.currentLadder.rect.right and entity.movement[0]:
						entity.onLadder = True

						#entity.rect.centerx = entity.currentLadder.rect.centerx
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

				if entity.currentLadder and (entity.rect.bottom < entity.currentLadder.rect.top):
					entity.onLadder = False
				if entity.currentLadder and ((entity.rect.left > entity.currentLadder.rect.right or entity.rect.right < entity.currentLadder.rect.left) ) :

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
					entity.onPlatform = False
	



	def update(self):
		if self.player.HP >0:
			self.checkCollisions(self.player)

			self.player.update(self.dt, self.screen_rect)		
			#Moves the tiles to give the illusion of player movement
			if self.player.camerax + self.player.movement_amount >= 0 and self.player.camerax <= self.player.maxx and  not self.player.onLadder:
				self.player.camerax += self.player.movement_amount
				for ladder in self.ladderList:
					ladder.rect.x -= self.player.movement_amount
				for platform in self.platform_boundaries_list:
					platform.rect.x -= self.player.movement_amount
				for platform in self.platform_draw_list:
					platform.rect.x -= self.player.movement_amount
				for knight in self.knightList:
					knight.rect.x -= self.player.movement_amount
				for item in self.set_props:
					item.x -= self.player.movement_amount
			elif self.player.camerax + self.player.movement_amount < 0:
				for ladder in self.ladderList:
					ladder.rect.x -= self.player.camerax
				for platform in self.platform_boundaries_list:
					platform.rect.x -= self.player.camerax
				for platform in self.platform_draw_list:
					platform.rect.x -= self.player.camerax
				for knight in self.knightList:
					knight.rect.x -= self.player.camerax
				for item in self.set_props:
					item.x -= self.player.camerax
				self.player.camerax = 0

			#knights
		for kUp in self.knightList:
			kUp.update(self.dt, self.screen_rect, self.player, self.knightList, self.platform_boundaries_list, self.ladderList)
			if kUp.invulTimer>0:
				kUp.invulTimer-=1
		self.checkCollisions(self.player)
		if self.player.invulTimer >0:
			self.player.invulTimer -=1

	def draw(self):
		#self.screen.fill((0,0,0))
		self.screen.blit(self.backgroundImage,self.screen_rect)
		self.counter = self.enemy_castle_entrence_rect.right
		while self.counter < self.player.maxx:
			self.screen.blit(self.castle_background_image, pygame.Rect(self.counter, 0, 800, 600))
			self.counter += 800
		#pygame.draw.line(self.screen,(0,0,0),(0,0),(300,300))
		for ladder in self.ladderList:
			ladder.draw(self.screen)
		self.counter = 0
		for platform in self.platform_draw_list:
			dirty = platform.rect.y + 20
			while dirty <= self.screen.get_rect().width:
				if platform.rect.x >= self.enemy_castle_entrence_rect.right:
					if self.dirt_type_list[self.counter] == 1:
							self.screen.blit (self.stone_image1, pygame.Rect(platform.rect.x, dirty, 40, 40))
					if self.dirt_type_list[self.counter] == 2:
						self.screen.blit (self.stone_image2, pygame.Rect(platform.rect.x, dirty, 40, 40))
					if self.dirt_type_list[self.counter] == 3:
						self.screen.blit (self.stone_image3, pygame.Rect(platform.rect.x, dirty, 40, 40))
					if self.dirt_type_list[self.counter] == 4:
						self.screen.blit (self.stone_image4, pygame.Rect(platform.rect.x, dirty, 40, 40))
				else:
					if self.dirt_type_list[self.counter] == 1:
						self.screen.blit (self.dirt_image1, pygame.Rect(platform.rect.x, dirty, 40, 40))
					if self.dirt_type_list[self.counter] == 2:
						self.screen.blit (self.dirt_image2, pygame.Rect(platform.rect.x, dirty, 40, 40))
					if self.dirt_type_list[self.counter] == 3:
						self.screen.blit (self.dirt_image3, pygame.Rect(platform.rect.x, dirty, 40, 40))
					if self.dirt_type_list[self.counter] == 4:
						self.screen.blit (self.dirt_image4, pygame.Rect(platform.rect.x, dirty, 40, 40))
				dirty += 40
				self.counter += 1
			platform.draw(self.screen)
		if self.player.invulTimer == 0:
			self.player.draw(self.screen)
		elif  random.random() > .2:
			self.player.draw(self.screen)
		#knights
		for kDraw in self.knightList:
			if kDraw.invulTimer == 0:
				kDraw.draw(self.screen)
			elif  random.random() > .2:
				kDraw.draw(self.screen)
			
			
		#Draw the castle gate last so it looks like everything is going through it
		self.screen.blit(self.castle_entrence_image, self.enemy_castle_entrence_rect)
		self.screen.blit(pygame.transform.flip(self.castle_entrence_image, True, False), self.good_castle_entrence_rect)
		self.screen.blit(pygame.image.load("../assets/Art/Bedsheet_Rope.png").convert_alpha(), pygame.Rect(self.good_castle_entrence_rect.right-32, -40, 32, 600))
