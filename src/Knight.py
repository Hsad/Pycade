import pygame, random, math

class Knight(object):
  def __init__(self, screen, xStart, yStart,enemyBool):

    pygame.font.init() #debug
    self.Dfont = pygame.font.Font(None, 40) #debug
    self.Dvar = 0 #debug
    self.debug1 = 0
    self.debug2 = 0    
    self.debug3 = 0
    self.debug4 = 0
    self.debug5 = 0

    self.spearRect = pygame.Rect(0,0,30,7)
    self.spearImg = pygame.image.load("../assets/Art/spear_temp.png").convert_alpha()
    self.direction = 0 #0 left, 1 right
    self.xpos = xStart	
    self.ypos = yStart #+ screen.get_rect().height
    self.midAir = False # weather or not player is in air, to set gravity of not
    self.usingSpear = False
    self.HP = 5
    self.invulTimer =100

    self.enemy = enemyBool

    if self.enemy == False:
      self.image = pygame.image.load("../assets/Art/knight_walk.png").convert_alpha() #allied 
    else:
      self.image = pygame.image.load("../assets/Art/enemy_knight_walk.png").convert_alpha() #enemy 
    #self.magicCubeImage = pygame.image.load("../assets/Art/PlayerDuckingPlaceholder.png") #debug
    #self.cubeRect = pygame.Rect(0,0,64,64) #debug
    #self.cubeRect.x = screen.get_rect().centerx #debug
    #self.cubeRect.y = screen.get_rect().centery #debug 
    
    self.rect = pygame.Rect(0,0,64,80)
    self.rect.x = self.xpos
    self.rect.y = self.ypos - self.rect.height
    #foot collider
    self.footBoxImg = pygame.image.load("../assets/Art/knightFootBox.png")
    self.footBoxRect =  pygame.Rect(0,0,32,20)
    self.footBoxRect.centerx = self.rect.x
    self.footBoxRect.centery = self.rect.bottom
    #left jumping collider
    self.leftBoxJumpImg = pygame.image.load("../assets/Art/knightLeftBox.png")
    self.leftBoxJump =  pygame.Rect(0,0,32,20)
    self.leftBoxJump.right = self.rect.left
    self.leftBoxJump.top = self.rect.centery
    #right jumping collider
    self.rightBoxJumpImg = pygame.image.load("../assets/Art/knightRightBox.png")
    self.rightBoxJump =  pygame.Rect(0,0,32,20)
    self.rightBoxJump.left = self.rect.right
    self.rightBoxJump.top = self.rect.centery
    #right fall prevention Collider
    self.rightPathFallImg = pygame.image.load("../assets/Art/knightRightBox.png")
    self.rightPathFall =  pygame.Rect(0,0,32,20)
    self.rightPathFall.left = self.rect.right
    self.rightPathFall.top = self.rect.bottom
    #left fall prevention collider
    self.leftPathFallImg = pygame.image.load("../assets/Art/knightLeftBox.png")
    self.leftPathFall =  pygame.Rect(0,0,32,20)
    self.leftPathFall.right = self.rect.left
    self.leftPathFall.top = self.rect.bottom
    #right possible jump Collider
    self.rightPosJumpImg = pygame.image.load("../assets/Art/knightRightBox.png")
    self.rightPosJump =  pygame.Rect(0,0,32,20)
    self.rightPosJump.left = self.rect.right
    self.rightPosJump.top = self.rect.centery
    #left possible jump collider
    self.leftPosJumpImg = pygame.image.load("../assets/Art/knightLeftBox.png")
    self.leftPosJump =  pygame.Rect(0,0,32,20)
    self.leftPosJump.right = self.rect.left
    self.leftPosJump.top = self.rect.centery

    self.movement = [False, False, False, False, True] #up down left right wander
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
    self.PRESISTANCE = random.randint(-100,100)
    self.pathing = False
    #values for sprite changes
    self.frame = 0
    self.framerate = 2
    self.framebuffer = 0

  def update(self, dt, screen_rect, player, knightList, platforms, ladders):
    if not self.pathing and ((self.playerNear(player) < 350 and not self.chasing) or (self.chasing and self.playerNear(player) < 650 + self.PRESISTANCE)):
      #if player is to the left or right of the knight
      self.chasing = True
      if player.rect.x > self.rect.x:
		self.movement[2]=False
		self.movement[3]=True
      else:
		self.movement[2]=True
		self.movement[3]=False      
      #if player is above or below knight
      if player.rect.y >= self.rect.y: #player is below knight
	self.movement[1]=True
	self.movement[0]=False
      elif player.rect.y < self.rect.y: #player is above
		self.movement[0]=True
		self.movement[1]=False
      else:
	self.movement[0]=False
	self.movement[1]=False
    elif not self.pathing: #if
      self.chasing = False
      self.movement[0]=False
      self.movement[1]=False
      self.movement[2]=False
      self.movement[3]=False
    self.checkSpearStab(player,knightList)
    #set preview hit box
    futureRect = self.rect.move(0,0)
    self.footBoxRect.centerx = futureRect.centerx
    self.footBoxRect.centery = futureRect.bottom

    self.leftBoxJump.right = futureRect.left
    self.leftBoxJump.top = futureRect.centery

    self.rightBoxJump.left = futureRect.right
    self.rightBoxJump.top = futureRect.centery


#Pathing checks
    if self.pathing:
	self.path(platforms, player)

    if self.movement[0] and self.chasing: #up
      if not self.playerAbove(player) or self.pathing: #player is far enough to the left or right of the knight to follow normaly
	#self.pathing = False
        """if not self.midAir: #on the ground
	  self.yvel = -300
	  self.midAir = True"""        
        for plat in platforms: #look for a low platform
	  if self.movement[3] and self.rightBoxJump.colliderect(plat.rect):
	    if not self.midAir: #on the ground
	      self.yvel = -300
	      self.midAir = True
	  elif self.movement[2] and self.leftBoxJump.colliderect(plat.rect):
	    if not self.midAir: #on the ground
	      self.yvel = -300
	      self.midAir = True
      else: #player is above knight, seek alt path
	self.pathing = True
	self.path(platforms, player)
	

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

  def checkSpearStab(self,player,knightList):
  	if (self.playerNear(player) < 150 and self.enemy):
  		self.usingSpear = True
  		if  self.direction == 1:
  			self.spearRect.x = self.rect.x - 30
  		else:
  			self.spearRect.x = self.rect.centerx + 30	
  		self.spearRect.y = self.rect.centery
  		if self.spearRect.colliderect(player.rect) and player.HP >0 and player.invulTimer<=0 and not player.ducking:

  			player.HP -=1
  			player.invulTimer = 100

  	else:
  		self.usingSpear = False

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
  
  def playerAbove(self, player):
    #the sighns are flipped between these two so the math is upright
    xDist = player.rect.centerx - self.rect.centerx 
    yDist = self.rect.centery - player.rect.top
    oa = 0
    if xDist != 0:
      oa = float(yDist) / float(xDist)
      #print "The next line should be a float"
      #print oa
    #else:
      #print "ERROR DIVIDE BY ZERO" 
    tanAngle = abs(math.degrees(math.atan(oa)))
    #print tanAngle
    if tanAngle < 60:
      return False
    else:
      return True

  def path(self, platforms, player):   
    if self.midAir:
      return
    if self.rect.centery <= player.rect.centery: #player is level with or below knight
      self.pathing = False

    leftSafe = True
    rightSafe = True
    leftJump = False
    rightJump = False
    for plat in platforms:
      for off in xrange(10):
	#is there something to jump on
	if rightSafe and self.rightPosJump.colliderect(plat.rect):#rightSafe and 
	  rightJump = True
	  break
	else:
	  self.rightPosJump.x += 40
	if leftSafe and self.leftPosJump.colliderect(plat.rect):#leftSafe and 
	  leftJump = True
	  break
	else:
	  self.leftPosJump.x -= 40
	#will i fall if I go this way
	if leftSafe and self.leftPathFall.colliderect(plat.rect):
	  self.leftPathFall.x -= 40
	else:
	  leftSafe = False
	  if self.debug5 == 0:#debug
	    self.debug5 = off#debug
	if rightSafe and self.rightPathFall.colliderect(plat.rect):
	  self.rightPathFall.x += 40
	else:
	  rightSafe = False
	
	

      self.leftPathFall.topright = self.rect.bottomleft
      self.rightPathFall.topleft = self.rect.bottomright
      self.leftPosJump.topright = self.rect.midleft
      self.rightPosJump.topleft = self.rect.midright
      if leftJump or rightJump:
	break

    #if jumpRight and jumpLeft:
    if rightJump:
      #set movement to right
      self.movement[3] = True
      self.movement[2] = False
      self.movement[4] = False
    elif leftJump:
      #set movement left
      self.movement[2] = True
      self.movement[3] = False      
      self.movement[4] = False
    else: #no where to go
      #set wander true <<<<<<<<<<<<<<<
      self.movement[4] = True
      #halt for now
      #self.movement[2]=False
      #self.movement[3]=False
    
    self.debug1 = leftJump
    self.debug2 = rightJump
    self.debug3 = leftSafe
    self.debug4 = rightSafe

  def draw(self,screen):
    #screen.blit(self.magicCubeImage, self.cubeRect)
    screen.blit(self.footBoxImg, self.footBoxRect)
    screen.blit(self.leftBoxJumpImg, self.leftBoxJump)
    screen.blit(self.rightBoxJumpImg, self.rightBoxJump)
    screen.blit(self.rightBoxJumpImg, self.rightPathFall)
    screen.blit(self.rightBoxJumpImg, self.leftPathFall)

    pygame.draw.line(screen, (0,200,0), self.rect.center, (self.rect.centerx + 81, self.rect.centery - 140)) 
    pygame.draw.line(screen, (0,200,0), self.rect.center, (self.rect.centerx - 81, self.rect.centery - 140))

    self.text = self.Dfont.render("leftJump "+str(self.debug1), 0, pygame.Color("red"), pygame.Color("black"))
    screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-50, 10,10))
    self.text = self.Dfont.render("rightJump "+str(self.debug2), 0, pygame.Color("red"), pygame.Color("black"))
    screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-100, 10,10))
    self.text = self.Dfont.render("pathing "+str(self.pathing), 0, pygame.Color("red"), pygame.Color("black"))
    screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-150, 10,10))    
    self.text = self.Dfont.render("leftSafe "+str(self.debug3), 0, pygame.Color("red"), pygame.Color("black"))
    screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-200, 10,10))
    self.text = self.Dfont.render("rightSafe "+str(self.debug4), 0, pygame.Color("red"), pygame.Color("black"))
    screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-250, 10,10))
    #self.text = self.Dfont.render("unsafeAfter "+str(self.debug5), 0, pygame.Color("red"), pygame.Color("black"))
    #screen.blit(self.text, pygame.Rect(self.rect.x,self.rect.y-275, 10,10))

    screen.blit(self.image, self.rect, pygame.Rect(64*(self.frame), self.direction*80, 64, 80))
    if self.usingSpear:
    	screen.blit(self.spearImg,self.spearRect)


