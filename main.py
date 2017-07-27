#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame
from pygame.locals import *
import random
import datetime
 
## Colores
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
MARTIS = (255, 192, 203)
GOLD = (255, 215, 0)
SKY_BLUE = (135,206,235)
MIDNIGHT_BLUE =	(25,25,112)
NAVY = (0,0,128)
BLUE = (0,0,255)
ORANGE = (255, 182, 2)
ALMOST_YELLOW = (255, 231, 2)

## Pantalla
WIDTH = 640
HEIGHT = 480

## Player
speedK = 3
playerBulletW = 15
playerBulletH = 10

## Star
NUM_STARS = 100
STAR_COLOUR = [WHITE, GOLD]

## Enemies
NUM_ENEMIES = 12
sizeEnemy = [20, 20]
enemyBulletW = 20
enemyBulletH = 15
dificult = 64

## Engine
ENGINE_COLOUR = [ORANGE, ALMOST_YELLOW]

#Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bulletsEnemy = pygame.sprite.Group()
engines = pygame.sprite.Group()
stars = pygame.sprite.Group()

# ---------------------------------------------------------------------
# Clases
# ---------------------------------------------------------------------
class redPixelClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     
        self.image = pygame.Surface([20, 15])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = 20
        self.rect.centery = HEIGHT/2 - 120
        self.speedx = speedK
        self.speedy = speedK
        self.colour = RED
        self.direction_shot = 1
    def update(self, time):
        ## Force drags you to the left
        self.drag_force()
        ## Update key event
        keys = pygame.key.get_pressed()
        ## Y AXIS
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speedy
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speedy
        ## X AXIS
        if self.rect.left >= 0:
            if keys[K_LEFT]:
                self.rect.centerx -= self.speedx
        if self.rect.right <= WIDTH:
            if keys[K_RIGHT]:
                self.rect.centerx += self.speedx
    def drag_force(self):
        ## Fuerza te arrastra hacia atras
        if self.rect.right <= (WIDTH):
            self.rect.centerx -= 0.5
        ## No puede salir izquierda
        if self.rect.left <= 0: 
            self.rect.centerx += 60     

    def shoot(self):
        bullet = BulletClass(playerBulletW, playerBulletH, self.rect.right, self.rect.y, self.direction_shot, self.colour)
        all_sprites.add(bullet)
        bullets.add(bullet)
    def engine(self, direction):
        engine = engineClass(self.rect.left, self.rect.bottom, MARTIS)
        engine.direction = direction 
        all_sprites.add(engine)
        engines.add(engine)

class starsClass(pygame.sprite.Sprite):
        def __init__(self, h, w, colour):
            pygame.sprite.Sprite.__init__(self)             
            self.image = pygame.Surface([w, h])
            self.image.fill(colour)
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH
            self.rect.centery = HEIGHT / 2
            self.speedx = 0.5
        def update(self, time):
            self.rect.centerx -= self.speedx * time   ## Variable with time
            ## Collision PARED
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.speedx = random.uniform(0.1, 1.5)
                self.rect.centerx = WIDTH + 10 
                self.rect.centery = random.randint(0, HEIGHT)

class enemyPixelClass(pygame.sprite.Sprite):
        def __init__(self, h, w, colour):
            pygame.sprite.Sprite.__init__(self)             
            self.image = pygame.Surface([w, h])
            self.image.fill(colour)
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH/2
            self.rect.centery = HEIGHT/2
            self.speedx = random.uniform(0.5, 7)
        def update(self, time):
            self.rect.centerx -= self.speedx
            ## Collision PARED
            if self.rect.left <= 0:
                self.rect.centerx = random.randrange(WIDTH, WIDTH + 100)
                self.rect.centery = random.randrange(0 + sizeEnemy[1], HEIGHT - self.rect.height, random.randint(1,self.rect.height))

class bluePixelClass(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)   
            self.colour = BLUE  
            self.image = pygame.Surface([80, 70])
            self.image.fill(self.colour)
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH - 90
            self.rect.centery = HEIGHT/2
            self.speedy = random.randint(4, 10)
            self.direction = 1
            self.life = 31
            self.dificult = dificult
            self.flagDifficult = True
        def update(self, time):
        	## Move
      		self.rect.centery += self.speedy * self.direction 
      		## Change color if hit
      		self.image.fill(self.colour)
      		## Shot!
      		if self.rect.centery % self.dificult == 0:
      			self.shoot()
      		## Update dificult
      		if self.life == 10 and self.flagDifficult == True :
      			self.speedy += 1
      			self.flagDifficult = False
      		if self.life == 30 and self.flagDifficult == False :
      			self.speedy += 1
      			self.flagDifficult = True
      		## Update position
      		if self.rect.bottom >= HEIGHT:
      			self.direction = -1
      		if self.rect.top <= 0:
      			self.direction = 1
      		## change colour
      		if self.life < 20:
      			if self.colour == BLUE:
      				self.colour = RED
      			else:
      				self.colour = BLUE
      	def shoot(self):
		    bullet = BulletClass(enemyBulletW, enemyBulletH, self.rect.left, self.rect.y, -1, BLUE)
		    all_sprites.add(bullet)
		    bulletsEnemy.add(bullet)

class BulletClass(pygame.sprite.Sprite):
        def __init__(self, w, h, x, y, direction, colour):
            pygame.sprite.Sprite.__init__(self)             
            self.image = pygame.Surface([w,h])
            self.image.fill(colour)
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
            self.speedx = 10
            self.direction = direction
        def update(self, time):
            self.rect.x += self.speedx * self.direction
            #kill if it moves off the top of the screen
            if self.rect.left > WIDTH:
                self.kill()
class engineClass(pygame.sprite.Sprite):
        def __init__(self,x,y, colour):
            pygame.sprite.Sprite.__init__(self)             
            self.image = pygame.Surface([8,8])
            self.image.fill(random.choice(ENGINE_COLOUR))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y
            self.speedx = 5
            self.speedy = 5
            self.direction = 0
            self.points = 20
        def update(self, time):
            if self.direction == K_RIGHT:
                self.rect.x -= self.speedx
            if self.direction == K_LEFT:
                self.rect.x += self.speedx
            if self.direction == K_UP:
                self.rect.y += self.speedy
            if self.direction == K_DOWN:
                self.rect.y -= self.speedy
            ## Update number of print points
            self.points -= 1 
            #kill if it moves off the top of the screen
            if self.points == 0:
                self.kill()   

# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
            raise SystemExit, message
    image = image.convert()
    if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
    return image

def crear_texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect

#---------------------------------------------------------------------
 
def main():
    ## Score variable
    score = 0
    ## Define screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Suanchelo spacegame")
    ## Call background image
    background_image = pygame.Surface(screen.get_size())
    background_image.fill(BLACK)
    ## Call spaceship and add to sprites group
    player = redPixelClass()
    all_sprites.add(player)
    ## Call "big" Enemy
    enemyBig = bluePixelClass()
    all_sprites.add(enemyBig)

    ## Call stars
    for n in range(NUM_STARS):
        star = starsClass(random.randint(2, 7),random.randint(3, 6), random.choice(STAR_COLOUR))
        star.rect.centery = random.randint(0, HEIGHT)
        star.rect.centerx = WIDTH
        star.speedx = 0.1 * random.uniform(0.1, 10)
        all_sprites.add(star)
        stars.add(star)

    ## Call enemies
    for n in range(NUM_ENEMIES):
	    enemy = enemyPixelClass(sizeEnemy[0], sizeEnemy[1], GREEN)
	    enemy.rect.centery = random.uniform(sizeEnemy[1], HEIGHT - sizeEnemy[1] )
	    enemy.rect.centerx = random.uniform(WIDTH - 2 * sizeEnemy[0], WIDTH + 200) 
	    enemy.speedx = 0.9 * random.uniform(0.1, 10)
	    all_sprites.add(enemy)
	    enemies.add(enemy)

    ## Clock
    clock = pygame.time.Clock()

    initFlag = True
    ## Init time
    start = datetime.datetime.now()
    text, text_rect = crear_texto('Red Pixel, Blue Pixel has stolen your girlfriend!', WIDTH/2, HEIGHT/2)
    textRed, textRed_rect = crear_texto('You, RED PIXEL', 140,HEIGHT/2 - 140, color = RED)
    textBlue, textBlue_rect = crear_texto('BLUE PIXEL', WIDTH - 120,HEIGHT/2 - 140, color = BLUE)

    speedx = 0
  
    ## Intro Loop
    while(initFlag):
        time = clock.tick(60)
        ## Background
        screen.blit(background_image, (0, 0))    
        stars.update(time)
        ## Text
        screen.blit(text, text_rect)
        screen.blit(textRed, textRed_rect)
        screen.blit(textBlue, textBlue_rect)
        ## Sprites                
        stars.draw(screen)    
        ## draw RedPixel
        pygame.draw.rect(screen,RED, (20,HEIGHT/2 - 120,20,15),0 )
        ## draw Blue Pixel
        pygame.draw.rect(screen,BLUE, (WIDTH - 90,HEIGHT/2 - 120,80,70),0 )
        ## draw Intro Pixel
        pygame.draw.rect(screen,MARTIS, (20,HEIGHT/2 + 20,speedx,15),0 )
        ## Update all changes
        pygame.display.flip()  
        ## End time
        stop = datetime.datetime.now()
        ## Move intro Pixel
        speedx += 1
        if stop - start >  datetime.timedelta(seconds=10):
            initFlag = False

    ## Main Loop
    runningFlag = True

    while runningFlag:
        time = clock.tick(60)
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
            elif eventos.type == pygame.KEYDOWN:
            	if eventos.key == pygame.K_SPACE:
            		player.shoot()
            elif eventos.type == pygame.KEYUP:
                if eventos.key == pygame.K_UP:
                	player.engine(K_UP)
                if eventos.key == pygame.K_DOWN:
                	player.engine(K_DOWN)
                if eventos.key == pygame.K_LEFT:
               		player.engine(K_LEFT)
               	if eventos.key == pygame.K_RIGHT:
               		player.engine(K_RIGHT)

        # 1. UPDATE POSITIONS
        all_sprites.update(time)
        text, text_rect = crear_texto('Score: ' + str(score), WIDTH-WIDTH/4, 40)       

        # 2. DETECT HITS
        ## 2.1 BulletPlayer - Enemy
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            enemy = enemyPixelClass(sizeEnemy[0], sizeEnemy[1], GREEN)
            enemy.rect.centery = random.uniform(sizeEnemy[1], HEIGHT - sizeEnemy[1] )
            enemy.rect.centerx = random.uniform(WIDTH - 2 * sizeEnemy[0], WIDTH + 200) 
            enemy.speedx += 2
            all_sprites.add(enemy)
            enemies.add(enemy)
            score += 1

        ## 2.2 Player - Enemy
        hit = pygame.sprite.spritecollide(player, enemies, True)
     	if hit:
            runningFlag = False

         ## 2.3 Player - EnemyBig
        hit = pygame.sprite.collide_rect(player, enemyBig)
        if hit:
            if enemyBig.life == 0:
        		runningFlag = False

       	## 2.4 Player - bulletEnemy
        hit = pygame.sprite.spritecollide(player, bulletsEnemy, True)
        if hit:
        	runningFlag = False

        ## 2.4 EnemyBig - bulletPlayer
        hit = pygame.sprite.spritecollide(enemyBig, bullets, True)
        if hit:
           	## Update life and dificult of the enemyBig
            score += 1
            enemyBig.life -= 1
            enemyBig.dificult -= 1 

            if enemyBig.life == 0:
        		runningFlag = False

        # 3. DRAW and UPDATE
        ## Background
        screen.blit(background_image, (0, 0))    
        ## Text
        screen.blit(text, text_rect)
        ## Sprites                
        all_sprites.draw(screen)                     
        ## Update all changes
        pygame.display.flip()

    endFlag = True

    if (enemyBig.life == 0):
    	text_end = "You save your girlfriend!"
    else:
   		text_end = "You've lost your girlfriend!"

    ## Init time
    start = datetime.datetime.now()
    text1, text_rect1 = crear_texto('Your score was: ' + str(score), WIDTH/2, HEIGHT/2)
    text2, text_rect2 = crear_texto(text_end, WIDTH/2, HEIGHT/2 + 50)
    ## Intro Loop
    while(endFlag):
        time = clock.tick(60)
        ## Background
        screen.blit(background_image, (0, 0))    
        stars.update(time)
        ## Text1
        screen.blit(text1, text_rect1)
        ## Text2
        screen.blit(text2, text_rect2)
        ## Sprites                
        stars.draw(screen)    
        ## Update all changes
        pygame.display.flip()  
        ## End time
        stop = datetime.datetime.now()

        if stop - start >  datetime.timedelta(seconds=10):
            endFlag = False

    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
