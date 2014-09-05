import pygame

class Player(object):
	def __init__(self, screen):
		self.xpos = 0
		self.ypos = screen.get_rect().height
		