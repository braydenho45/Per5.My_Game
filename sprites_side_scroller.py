# This file was created by: Brayden Ho

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint

vec = pg.math.Vector2



# create the player class with a superclass of Sprite
class Player(Sprite):
    # this initializes the properties of the player class including the x y location, and the game parameter so that the the player can interact logically with
    # other elements in the game...
    def __init__(self, game, x, y):
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
        self.speed = 1
        # self.vx, self.vy = 0, 0
        self.coin_count = 0
        self.jump_power = 20
        self.jumping = False
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
        if keys[pg.K_f]:
            self.shoot()
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
        direction = vec(1,0)
        Bullet(self.game, self.rect.centerx, self.rect.centery, direction)
            
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
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 25

    def update(self):
        self.rect.x += self.speed
        # self.rect.y += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0

        hits = pg.sprite.spritecollide(self, self.game.all_bullets, True)
        if hits:
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
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Bullet(Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites, game.all_bullets
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))  # Bullet size
        self.image.fill(RED)  # Bullet color
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction

    def update(self):
        # Move the bullet in the direction
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
        