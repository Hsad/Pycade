import pygame, sys, Player

class Game(object):
	def __init__(self):
		pygame.init()
		self.over = False
		self.screen = pygame.display.set_mode((800,600))
		self.screen_rect = self.screen.get_rect()
		self.player = Player.Player(self.screen)
		self.clock = pygame.time.Clock();
		self.timer = pygame.time.get_ticks()
		self.dt = 0
		pygame.display.set_caption("A Team Won Game ")
		self.backgroundImage = pygame.image.load("../assets/BackgroundPlaceholder.jpg").convert_alpha()
		self.backgroundRect = self.backgroundImage.get_rect()

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

		print self.player.movement


	def update(self):
		self.player.update(self.dt, self.screen_rect)

	def draw(self):
		#self.screen.fill((0,0,0))
		self.screen.blit(self.backgroundImage,self.screen_rect)
		#pygame.draw.line(self.screen,(0,0,0),(0,0),(300,300))

		self.player.draw(self.screen)

