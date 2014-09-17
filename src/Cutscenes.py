import pygame, sys, Player

class Cutscenes(object):

	def __init__ (self):
		self.screen = pygame.display.set_mode((800, 600))
		
		self.current_state = "Team Logo"
		
		#Team Logo Animation Pieces
		self.logo_animation_start = pygame.image.load("../assets/Art/Logo_Entrence_Animation.png").convert_alpha()
		self.logo_still = pygame.image.load("../assets/Art/Team_Logo.png").convert_alpha()
		self.logo_frame = 0
		
		self.menu_background = pygame.image.load("../assets/Art/Castle_Background.png").convert_alpha()
		self.player = Player.Player(self.screen)
		self.player.rect.left = self.screen.get_rect().width/2+100
		self.player.rect.bottom = self.screen.get_rect().height
		self.knight_image = pygame.image.load("../assets/Art/knight_walk.png")
		self.knight_rect = pygame.Rect(0, 0, 64, 80)
		self.knight_rect.bottom = 600
		self.knight_rect.left = self.screen.get_rect().width/2-100
		self.knight_frame = 0
		
		self.enter_pressed = False
		
	def check_keys(self):
		#Check to see if the player has pressed space or enter
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						sys.exit()
					if event.key == pygame.K_SPACE:
						self.enter_pressed = True
					else:
						self.enter_pressed = False
		
	def main_menu(self):
		#Check if we hit enter to skip the intro, and move on to the next task
		#if we haven't
		while True:
			
			self.check_keys()
			if self.enter_pressed:
				break
			
			if self.current_state == "Team Logo":
				#Draw the logo animation
				self.screen.blit(pygame.image.load("../assets/Art/Intro_Animation_Background.png").convert_alpha(), pygame.Rect(0, 0, 800, 600))
				if self.logo_frame <= 16:
					self.screen.blit(self.logo_animation_start, pygame.Rect(0, 0, 800, 600), pygame.Rect(800*(self.logo_frame/2), 0, 800, 600))
				elif self.logo_frame <= 86:
					self.screen.blit(self.logo_still, pygame.Rect(0, 0, 800, 600))
				elif self.logo_frame == 111:
					self.current_state = "Conversation"
					
				self.logo_frame += 1
			
			if self.current_state == "Conversation":
				self.screen.blit(self.menu_background, pygame.Rect(0, 0, 800, 600))
				self.screen.blit(self.knight_image, self.knight_rect, pygame.Rect(64, 0, 64, 80))
				
				print self.player.rect.x
				self.player.draw(self.screen)
				
			
			pygame.display.flip()