from environment_assets import *

# Creating Sprites for all objects
AllSprites = pygame.sprite.Group()
# LightSpears shot by Galacticans
LightSpears = pygame.sprite.Group()
# Blacknites work for OverLord
BlackNites = pygame.sprite.Group()
# BlackSpears shot by Slaves
BlackSpears = pygame.sprite.Group()

# creating 1st person player
class Galactican(pygame.sprite.Sprite):
    # Galactican who saves the galaxy
    # sprite for the player
    def __init__(self, player_name="Galactican"):
        pygame.sprite.Sprite.__init__(self)
        # self.image and self.rect is a must for sprites to work
        self.name = player_name
        self.image = player_animation["straight"]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # gets the bounding rectangle of the player image
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.xspeed = 0
        self.radius = int(self.rect.width*0.75/2)
        self.shield = GALACTIAN_SHIELDS
        self.shoot_delay = 250 # milliseconds wait till next shot
        self.last_time_shot = pygame.time.get_ticks()
        self.frame_rate = FPS
        self.frame = 0
        self.last_updated = pygame.time.get_ticks()
        self.left_moving = False
        self.right_moving = False

    def reset_image(self):
        center = self.rect.center
        self.image = player_animation["straight"]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0

    def move(self, side):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_updated >= self.frame_rate:
            self.last_updated = current_time
            if self.frame >= (len(player_animation[side])-1):
                pass
            else:
                center = self.rect.center
                self.image = player_animation[side][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.frame += 1

    def update(self):
        # always set the acceleration to 0 during update
        self.xspeed = 0
        # check for the keypressed state
        keyState = pygame.key.get_pressed()
        # controls for keypressed
        if keyState[pygame.K_LEFT]:
            self.xspeed = -10
            self.left_moving = True
            self.right_moving = False
        elif keyState[pygame.K_RIGHT]:
            self.xspeed = 10
            self.right_moving = True
            self.left_moving = False
        else:
            self.left_moving = False
            self.right_moving = False
        if keyState[pygame.K_SPACE]:
            self.shoot()
        # animation
        if self.left_moving:
            self.move("left")
        elif self.right_moving:
            self.move("right")
        else:
            self.reset_image()
        # updating the displacement
        self.rect.x += self.xspeed
        # setup the boundaries
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_shot >= self.shoot_delay:
            self.last_time_shot = current_time
            shoot_sound.play()
            lightspear = LightSpear(self.rect.centerx, self.rect.top)
            AllSprites.add(lightspear)
            LightSpears.add(lightspear)
    
    def space_crash(self):
        self.shield -= 10
        if self.shield <= 0:
            return False
        else:
            return True
    
    def spear_crash(self):
        self.shield -= 4
        if self.shield <= 0:
            return False
        else:
            return True

class Slave(pygame.sprite.Sprite):
    # Slaves of the OverLord who work for him tiredlessly
    # evil creatures
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = choice(blacknite)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.bottom = self.random_position()
        self.xspeed, self.yspeed = self.random_speed()
        self.radius = int(self.rect.width*0.75/2)
        self.shield = GALACTIAN_SHIELDS
        self.shoot_delay = 2000 # milliseconds wait till next shot
        self.last_time_shot = pygame.time.get_ticks()
    
    def random_position(self):
        topx = randrange(0, WIDTH-self.rect.width)
        bottom = 0
        return topx, bottom
    
    def random_speed(self):
        xspeed = randrange(-5, 5)
        yspeed = randrange(5, 10)
        return xspeed, yspeed

    def randomiseLocation(self):
        self.rect.x, self.rect.bottom = self.random_position()
        self.xspeed, self.yspeed = self.random_speed()

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        self.shoot()
        if self.rect.top >= HEIGHT:
            self.randomiseLocation()
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_shot >= self.shoot_delay:
            self.last_time_shot = current_time
            shoot_sound.play()
            blackspear = BlackSpear(self.rect.centerx, self.rect.bottom)
            AllSprites.add(blackspear)
            BlackSpears.add(blackspear)
        

class LightSpear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = yellowspear
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.yspeed = -10
    
    def update(self):
        self.rect.y += self.yspeed
        if self.rect.bottom < 0:
            self.kill()

class BlackSpear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = redspear
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.yspeed = 10
    
    def update(self):
        self.rect.y += self.yspeed
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = animated_explosion[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame_rate = FPS
        self.frame = 0
        self.last_updated = pygame.time.get_ticks()
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_updated >= self.frame_rate:
            self.last_updated = current_time
            self.frame += 1
            if self.frame == len(animated_explosion[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = animated_explosion[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def explosion_animation(strike, size):
    blacknite_explosion.play()
    explosion = Explosion(strike.rect.center, size)
    AllSprites.add(explosion)

def NewSlave():
    slave = Slave()
    AllSprites.add(slave)
    BlackNites.add(slave)