import pygame, sys, Player

class Game(object):
	def __init__(self):
		pygame.init()
		self.over = False
		self.screen = pygame.display.set_mode((800,600))
		self.player = Player.Player(self.screen)
		self.clock = pygame.time.Clock();
		self.timer = pygame.time.get_ticks()
		self.dt = 0
		#self.elapsed = 0


	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					self.over = True
					
					sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.over = True

	def update(self):
		pass

	def draw(self):
		pass

