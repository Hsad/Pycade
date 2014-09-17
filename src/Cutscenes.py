import pygame, sys, Player

class Cutscenes(object):

	def __init__ (self):
		self.screen = pygame.display.set_mode((800, 600))
		
		self.current_state = "Team Logo"
		self.font= pygame.font.Font(None,20)
		self.text = self.font.render("", 0, pygame.Color("red"), pygame.Color("black"))
		self.text2 = self.font.render("", 0, pygame.Color("red"), pygame.Color("black"))
		self.text3 = self.font.render("", 0, pygame.Color("red"), pygame.Color("black"))

		self.text4 = self.font.render("", 0, pygame.Color("red"), pygame.Color("black"))

		self.text5 = self.font.render("", 0, pygame.Color("red"), pygame.Color("black"))

		self.title_image = pygame.image.load("../assets/Art/royalrescue.png").convert_alpha()

		self.imageRect = self.title_image.get_rect()
		self.imageRect.x = 200
		self.imageRect.y = 100
		
		
		#Team Logo Animation Pieces
		self.logo_animation_start = pygame.image.load("../assets/Art/Logo_Entrence_Animation.png").convert_alpha()
		self.logo_still = pygame.image.load("../assets/Art/Team_Logo.png").convert_alpha()
		self.logo_frame = 0
		
		self.menu_background = pygame.image.load("../assets/Art/Castle_Background.png").convert_alpha()
		self.player = Player.Player(self.screen)
		self.player.state = 1
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
				self.screen.blit(self.player.image, self.player.rect, pygame.Rect(64*(self.player.frame), (2*self.player.state + 1) * 80 , 64, 80))
				self.screen.blit(self.title_image,self.imageRect)

				#self.player.draw(self.screen)
				
				
				self.text = self.font.render("I understand your concern Princess, but unfortunately I cannot oblige.", 0, pygame.Color("red"), pygame.Color("black"))
				self.screen.blit(self.text, pygame.Rect(250,250, 10,10))
				self.text2 = self.font.render("The knights who have captured your brother are known for their viciousness", 0, pygame.Color("red"), pygame.Color("black"))
				self.screen.blit(self.text2, pygame.Rect(250,265, 10,10))
				self.text3 = self.font.render("and it would not be fitting of me as a protector of hte royal family if I", 0, pygame.Color("red"), pygame.Color("black"))
				self.screen.blit(self.text3, pygame.Rect(250,280, 10,10))				
				self.text4 = self.font.render("allowed you to put yourself in harm's way.", 0, pygame.Color("red"), pygame.Color("black"))
				self.screen.blit(self.text4, pygame.Rect(250,295, 10,10))	
				self.text5 = self.font.render("Do not worry.  I assure you I will see to the prince's swift return.", 0, pygame.Color("green"), pygame.Color("black"))
				self.screen.blit(self.text5, pygame.Rect(250,310, 10,10))
			pygame.display.flip()