import pygame

class Knight(object):
  def __init__(self, screen):
    self.direction = 0 #0 left, 1 right
    self.xpos = 0
    self.ypos = screen.get_rect().height

    self.image = pygame.image.load("../assets/Art/knight_walk.png").convert_alpha()
    self.rect = pygame.Rect(0,0,64,80)
    self.rect.x = self.xpos
    self.rect.y = self.ypos - self.rect.height

    self.movement = [False, False, False, True] #up down left right
    self.xvel = 0
    self.yvel = 0

    #acceleration and deceleration
    self.xaccel = 50
    self.gravity = 700
    self.xdecel = 100

    #max horizontal speed
    self.xmax = 50

    #values for sprite changes
    self.frame = 0
    self.framerate = 2
    self.framebuffer = 0

  def update(self, dt, screen_rect):
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
      if self.xvel < self.xmax:
	self.xvel = self.xmax    

    if self.movement[2] == self.movement[3]:
      self.deceleration("x", dt)

    future_rect.x += self.xvel*dt
    future_rect.y += self.yvel*dt

    #bound check
    if future_rect.right > screen_rect.right + 500:
      future_rect.right = screen_rect.right + 500
      self.xvel = 0
      self.movement[3] = False
      self.movement[2] = True
    if future_rect.left <  -500:
      future_rect.left =  -500
      self.xvel = 0
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
