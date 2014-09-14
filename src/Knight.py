import pygame, random

class Knight(object):
  def __init__(self, screen, xStart, yStart):

    pygame.font.init() #debug
    self.Dfont = pygame.font.Font(None, 40) #debug
    self.Dvar = 0 #debug

    self.direction = 0 #0 left, 1 right
    self.xpos = xStart
    self.ypos = yStart + screen.get_rect().height

    self.image = pygame.image.load("../assets/Art/knight_walk.png").convert_alpha()
    self.magicCubeImage = pygame.image.load("../assets/Art/PlayerDuckingPlaceholder.png") #debug
    self.cubeRect = pygame.Rect(0,0,64,64) #debug
    self.cubeRect.x = screen.get_rect().centerx #debug
    self.cubeRect.y = screen.get_rect().centery #debug 
    self.rect = pygame.Rect(0,0,64,80)
    self.rect.x = self.xpos
    self.rect.y = self.ypos - self.rect.height

    self.movement = [False, False, False, True] #up down left right
    self.xvel = 0
    self.yvel = 0

    #acceleration and deceleration
    self.xaccel = 200 + random.randint(-20,20)
    self.gravity = 700
    self.xdecel = 500 + random.randint(-20,20)

    self.jumping = False

    #max horizontal speed
    self.xmax = 200 + random.randint(-20,20)

    #values for sprite changes
    self.frame = 0
    self.framerate = 2
    self.framebuffer = 0

  def update(self, dt, screen_rect, player):

    if player.rect.x > self.rect.x:
      self.movement[2]=False
      self.movement[3]=True
    else:
      self.movement[2]=True
      self.movement[3]=False      

    future_rect = self.rect.move(0,0)

    if self.movement[2]: #left
      if self.xvel > 0:
	self.xvel-=self.xdecel*dt
      else:
	self.xvel-=self.xaccel*dt
	self.direction = 1
      if self.xvel < -self.xmax:
	self.xvel = -self.xmax


    if self.movement[3]: #right
      if self.xvel < 0:
	self.xvel+=self.xdecel*dt
      else:
	self.xvel+=self.xaccel*dt
	self.direction = 0
      if self.xvel > self.xmax:
	self.xvel = self.xmax    

    if self.movement[2] == self.movement[3]:
      self.deceleration("x", dt)

    future_rect.x += self.xvel*dt
    future_rect.y += self.yvel*dt

    self.cubeRect.x -= self.xvel

    #bound check
    if future_rect.right > screen_rect.right + 100:
      self.movement[3] = False
      self.movement[2] = True
    if future_rect.left < screen_rect.left - 100:
      self.movement[3] = True
      self.movement[2] = False
    if future_rect.top < 0:
      future_rect.top = 0
    if future_rect.bottom > screen_rect.bottom:
      future_rect.bottom = screen_rect.bottom

    self.rect = future_rect

    #sprite changing
    if self.movement == [False, False, False, False]:
      self.frame = 0
    else:
      self.framebuffer += dt
      if self.framebuffer > .5/self.framerate:
	self.framebuffer = 0
	self.frame += 1
      if self.frame > 3:
	self.frame = 0

  def deceleration(self, dimension, dt):
    if dimension == "x":
      if self.xvel < 0:
	self.xvel += self.xdecel*dt
	if self.xvel > 0:
	  self.xvel = 0
      if self.xvel > 0:
	self.xvel -= self.xdecel*dt
	if self.xvel < 0:
	  self.xvel = 0

  def draw(self,screen):
    screen.blit(self.image, self.rect, pygame.Rect(64*(self.frame), self.direction*80, 64, 80)) 
    #screen.blit(self.magicCubeImage, self.cubeRect)
    #self.text = self.Dfont.render(str(self.xvel), 0, pygame.Color("red"), pygame.Color("black"))
    screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-50, 10,10))
    #self.text = self.Dfont.render(str(self.rect.x), 0, pygame.Color("red"), pygame.Color("black"))
    screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-100, 10,10))
