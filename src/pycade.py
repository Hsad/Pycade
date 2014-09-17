import pygame, sys, Game, Cutscenes

g = Game.Game()
c = Cutscenes.Cutscenes()
c.main_menu()
while not g.over:
	#divide by 1000 to allow for more difference in speed
	g.dt = g.clock.tick(60)/1000.0
	g.process_events()
	g.update()
	g.draw()
	pygame.display.flip()
