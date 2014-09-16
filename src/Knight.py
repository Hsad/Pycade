import pygame, random, math

class Knight(object):
  def __init__(self, screen, xStart, yStart):

    pygame.font.init() #debug
    self.Dfont = pygame.font.Font(None, 40) #debug
    self.Dvar = 0 #debug

    self.direction = 0 #0 left, 1 right
    self.xpos = xStart	
    self.ypos = yStart #+ screen.get_rect().height
    self.midAir = False # weather or not player is in air, to set gravity of not

    self.enemy = False
    if self.enemy == False:
      self.image = pygame.image.load("../assets/Art/knight_walk.png").convert_alpha() #allied 
    else:
      self.image = pygame.image.load("../assets/Art/knight_walk.png").convert_alpha() #enemy (not implemented)
    #self.magicCubeImage = pygame.image.load("../assets/Art/PlayerDuckingPlaceholder.png") #debug
    #self.cubeRect = pygame.Rect(0,0,64,64) #debug
    #self.cubeRect.x = screen.get_rect().centerx #debug
    #self.cubeRect.y = screen.get_rect().centery #debug 
    
    self.rect = pygame.Rect(0,0,64,80)
    self.rect.x = self.xpos
    self.rect.y = self.ypos - self.rect.height
    
    self.footBoxImg = pygame.image.load("../assets/Art/knightFootBox.png")
    self.footBoxRect =  pygame.Rect(0,0,32,20)
    self.footBoxRect.centerx = self.rect.x
    self.footBoxRect.centery = self.rect.bottom

    self.movement = [False, False, False, False] #up down left right
    self.xvel = 0
    self.yvel = 0

    #acceleration and deceleration
    self.xaccel = 200 + random.randint(-20,20)
    self.gravity = 700
    self.xdecel = 500 + random.randint(-20,20)

    self.jumping = False

    #max horizontal speed
    self.xmax = 200 + random.randint(-20,20)

    #max line of sight
    self.MAXSIGHT = 500
    self.chasing = False
    #values for sprite changes
    self.frame = 0
    self.framerate = 2
    self.framebuffer = 0

  def update(self, dt, screen_rect, player, knightList, platforms, ladders):
    if (self.playerNear(player) < 300 and not self.chasing) or (self.chasing and self.playerNear(player) < 500):
      #if player is to the left or right of the knight
      self.chasing = True
      if player.rect.x > self.rect.x:
	self.movement[2]=False
	self.movement[3]=True
      else:
	self.movement[2]=True
	self.movement[3]=False      
      #if player is above or below knight
      if player.rect.y > self.rect.y: #player is below knight
	self.movement[1]=True
	self.movement[0]=False
      elif player.rect.y < self.rect.y: #player is above
	self.movement[0]=True
	self.movement[1]=False
      else:
	self.movement[0]=False
	self.movement[1]=False
    else: #if self.playerNear(player) > 200 and self.chasing:
      self.chasing = False
      self.movement[0]=False
      self.movement[1]=False
      self.movement[2]=False
      self.movement[3]=False

    #set preview hit box
    futureRect = self.rect.move(0,0)
    self.footBoxRect.centerx = futureRect.centerx
    self.footBoxRect.centery = futureRect.bottom


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

    if self.movement[0]: #up
      """if not self.midAir: #on the ground
	self.yvel = -300
	self.midAir = True"""
      #look for a ladder
      #if found move tward ladder
      #if on ladder, move up

    if self.midAir: #falling gravity or not
      self.yvel += self.gravity*dt
    else:
      self.yvel = 0

    if self.movement[2] == self.movement[3]:
      self.deceleration("x", dt)

    futureRect.x += self.xvel*dt
    futureRect.y += self.yvel*dt

    #self.cubeRect.x -= self.xvel

    #bound check
    if futureRect.right > screen_rect.right + 100:
      self.movement[3] = False
      self.movement[2] = True
    if futureRect.left < screen_rect.left - 100:
      self.movement[3] = True
      self.movement[2] = False
    if futureRect.top < 0:
      futureRect.top = 0
    if futureRect.bottom >= screen_rect.bottom:
      futureRect.bottom = screen_rect.bottom
 

    #foot bounds
    tempMidAir = True
    for plat in platforms:
      if self.footBoxRect.colliderect(plat.rect): #feet are colliding with a platform
	if self.midAir == True: #just landing
	  if self.footBoxRect.centery > plat.rect.top: #hit box is colliding and feet are down below plat
	    tempMidAir = False
	    futureRect.bottom = plat.rect.top
	if self.midAir == False:
	  tempMidAir = False
    
    if self.footBoxRect.centery >= screen_rect.bottom: #stop knights from falling through the bottom of the screen
      tempMidAir = False
    
    self.midAir = tempMidAir

    #update location
    self.rect = futureRect
    
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

  def playerNear(self, player):
    xDist = abs(player.rect.x - self.rect.x)
    yDist = abs(player.rect.y - self.rect.y)
    dist = math.sqrt(xDist*xDist + yDist*yDist)
    if dist < self.MAXSIGHT:
      return dist
    else:
      return dist

  def draw(self,screen):
    #screen.blit(self.magicCubeImage, self.cubeRect)
    screen.blit(self.footBoxImg, self.footBoxRect)
    #self.text = self.Dfont.render(str(self.yvel), 0, pygame.Color("red"), pygame.Color("black"))
    #screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-50, 10,10))
    #self.text = self.Dfont.render(str(self.midAir), 0, pygame.Color("red"), pygame.Color("black"))
    #screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-100, 10,10))
    #screen.blit(self.image, self.rect, pygame.Rect(64*(self.frame), self.direction*80, 64, 80))

