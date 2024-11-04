# This file was created by: Brayden Ho

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint

vec = pg.math.Vector2

# defines the health bar function
def draw_health_bar(surface, x, y, health, max_health):
        # length and width of bar
        bar_length = 30
        bar_height = 15
        # percentage of current health based on max health
        fill = (health / max_health) * bar_length
        #outline of health bar
        outline_rect = pg.Rect(x, y, bar_length, bar_height)
        # filled portion of bar
        fill_rect = pg.Rect(x, y, fill, bar_height)
        # if health is over half, bar is green
        if health > max_health * 0.5:
            color = GREEN
        # if health is below 50 but less than 20, bar is yellow
        elif health > max_health * 0.2:
            color = pg.Color('yellow')
        # if health is below 20, bar is red
        else:
            color = RED
        pg.draw.rect(surface, color, fill_rect)
        # draws white border around health bar
        pg.draw.rect(surface, WHITE, outline_rect, 2)

# create the player class with a superclass of Sprite
class Player(Sprite):
    # this initializes the properties of the player class including the x y location, and the game parameter so that the the player can interact logically with
    # other elements in the game...
    def __init__(self, game, x, y):
        self.can_shoot = True
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        # self.vx, self.vy = 0, 0
        self.coin_count = 0
        self.jump_power = 20
        self.jumping = False
        # health attributes
        self.health = 100 
        self.max_health = 100
    def get_keys(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.vy -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= 1
        # if keys[pg.K_s]:
        #     self.vy += self.speed
        if keys[pg.K_d]:
            self.vel.x += 1
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_f] and self.can_shoot: # ensures the bullet is only shot when it is true
            self.shoot()
            self.can_shoot = False
        if not keys[pg.K_f]:
            self.can_shoot = True # key that is used to fire the bullet
    def jump(self):
        print("im trying to jump")
        print(self.vel.y)
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
            print('still trying to jump...')

    def shoot(self):
        direction = vec(1,0) # determines the space between each bullet
        Bullet(self.game, self.rect.centerx, self.rect.centery, direction) # determines location of bullet and the direction it is being fired at
            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
                # print("Collided on x axis")
        #     else:
        #         print("not working...for hits")
        # # else:
        #     print("not working for dir check")
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                self.speed += 20
                print("I've gotten a powerup!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("I got a coin!!!")
                self.coin_count += 1

    def update(self):
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc

        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        # teleport the player to the other side of the screen
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)

# added Mob - moving objects
# it is a child class of Sprite
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32)) # Mob Size
        self.image.fill(PINK) # Mob color
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10
        self.health = 100
        self.max_health = 100

    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

        hits = pg.sprite.spritecollide(self, self.game.all_bullets, True) # the hits defines if the bullet hits the enemy, the enemy will die 
        if hits:
            # health taken per hit
            self.health -= 20
            # health below or equal to 0, kill mob
            if self.health <= 0:
                self.kill()

        if self.rect.colliderect(self.game.player):
            self.speed *= -1

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)) # coin size
        self.image.fill(GOLD) # coin color
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE # sets the sprite to a certain point on x axis based on tilsize
        self.rect.y = y * TILESIZE # sets the sprite to a certain point on y axis based on tilsize

class Bullet(Sprite):
    def __init__(self, game, x, y, direction): # defining the bullet class
        self.groups = game.all_sprites, game.all_bullets # assigns the sprite to two groups
        Sprite.__init__(self, self.groups) # makes it apart of pygames sprite system
        self.game = game
        self.image = pg.Surface((10, 10))  # Bullet size
        self.image.fill(RED)  # Bullet color
        self.rect = self.image.get_rect() # gets the area of the bullet. which is used for collision
        self.rect.center = (x, y) # sets the inital position of the bullet
        self.speed = 10 # Bullet speed
        self.direction = direction # defines the direction the bullet will move in 

    def update(self):
        self.rect.x += self.speed * self.direction.x # updates the bullets position based on speed and direction
        self.rect.y += self.speed * self.direction.y 
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT: # determines if the bullet is moved off screen, causing it to be killed
            self.kill()



        