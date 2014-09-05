import pygame, sys, Game

g = Game.Game()
while not g.over:
	g.clock.tick(60)
	g.process_events()
	g.update()
	g.draw()
	pygame.display.flip()