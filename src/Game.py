import pygame

class Game(object):
	def __init__(self):
		pygame.init()
		self.over = False
		self.clock = pygame.time.Clock();
		self.screen = pygame.display.set_mode((1024,768))
		self.timer = pygame.time.get_ticks()
		self.elapsed = 0


	def process_events(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.over = True

	def update(self):
		self.elapsed = pygame.time.get_ticks() - self.timer
		self.timer = pygame.time.get_ticks()
		print self.elapsed

	def draw(self):
		pass

