import pygame, math

class Camera(object):
	def __init__(self, player):
		self.x = 0
		self.y = 0

		#bouding box
		self.radius = 30

	def update(self, player, screen):
		pass