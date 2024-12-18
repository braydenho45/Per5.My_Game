# This file was created by: Brayden Ho

import random
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
        fill = max(0, (health / max_health) * bar_length)
        #outline of health bar
        outline_rect = pg.Rect(x, y, bar_length, bar_height)
        # filled portion of bar
        fill_rect = pg.Rect(x, y, fill, bar_height)
        background_color = pg.Color('black')
        pg.draw.rect(surface, background_color, outline_rect)
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
        super().__init__(game.all_sprites)  
        self.game = game
        self.image = pg.image.load("images/player.gif")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x * TILESIZE, y * TILESIZE)
        self.pos = vec(self.rect.center)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 10
        self.coin_count = 0
        self.jump_power = 12
        self.jumping = False
        self.health = 100 
        self.max_health = 100
        self.can_shoot = True
        self.facing = vec(1, 0)
        self.last_hit_time = 0
        self.invincibility_time = 0  # Timer for invincibility

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        while hits:
            self.pos.y -= 1
            self.rect.midbottom = self.pos
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)

    def get_keys(self):
        keys = pg.key.get_pressed()
        self.acc = vec(0, GRAVITY)
        # if keys[pg.K_w]:
        #     self.vy -= self.speed
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_ACC
            self.facing = vec(-1,0)
            self.image = pg.transform.flip(self.original_image, True, False)
        # if keys[pg.K_s]:
        #     self.vy += self.speed
        elif keys[pg.K_d]:
            self.vel.x = PLAYER_ACC
            self.facing = vec(1,0)
            self.image = self.original_image
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_f] and self.can_shoot: # ensures the bullet is only shot when it is true
            self.shoot()
            self.can_shoot = False
        elif not keys[pg.K_f]:
            self.can_shoot = True # key that is used to fire the bullet

    def jump(self):
        print("im trying to jump")
        print(self.vel.y)
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
            print('still trying to jump...')

    def shoot(self):
        if self.facing.length() == 0:
            self.facing = vec(1,0)
        Bullet(self.game, self.rect.centerx, self.rect.centery, self.facing) # determines location of bullet and the direction it is being fired at
            
    def collide_with_walls(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            for hit in hits:
                if dir == 'x':
                    if self.vel.x > 0:
                        self.pos.x = hit.rect.left - self.rect.width 
                    elif self.vel.x < 0:
                        self.pos.x = hit.rect.right 
                    self.vel.x = 0
                elif dir == 'y':
                    if self.vel.y > 0:
                        self.pos.y = hit.rect.top - self.rect.height
                        self.jumping = False
                    elif self.vel.y < 0:
                        self.pos.y = hit.rect.bottom 
                    self.vel.y = 0
        self.rect.topleft = self.pos

    def take_damage(self, amount):
        now = pg.time.get_ticks()
        if now - self.invincibility_time > 1000:  # Invincible for 1 second after damage
            self.health -= amount
            self.invincibility_time = now  # Reset invincibility timer
            if self.health <= 0:
                print("Player has died!")
                self.kill()

    def update(self):
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.rect.topleft = self.pos

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("images/enemy.gif")
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 2.5
        self.health = 100
        self.max_health = 100
        self.last_shot = pg.time.get_ticks()
        self.shoot_cooldown = 5000
        self.facing_left = True

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_cooldown:
            self.last_shot = now
            direction = pg.math.Vector2(self.game.player.rect.centerx - self.rect.centerx,self.game.player.rect.centery - self.rect.centery)
            if direction.length() > 0:  # Check for zero-length vector
                direction = direction.normalize()
                MobBullet(self.game, self.rect.centerx, self.rect.centery, direction)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self):
        player_pos = self.game.player.rect.center
        mob_pos = self.rect.center
        direction = pg.math.Vector2(player_pos[0] - mob_pos[0], player_pos[1] - mob_pos[1])
        if direction.length() > 0:
            direction = direction.normalize()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed     
        self.shoot()
        if self.rect.colliderect(self.game.player.rect):
            now = pg.time.get_ticks()
            if now - self.game.player.last_hit_time > 500:
                self.game.player.take_damage(10)  # Inflict damage on the player
                self.game.player.last_hit_time = now
        hits = pg.sprite.spritecollide(self, self.game.all_bullets, True) # the hits defines if the bullet hits the enemy, the enemy will die 
        for _ in hits:
           self.take_damage(50)

class MobBullet(Sprite):
    def __init__(self, game, x, y, direction):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("images/bullet.gif")  # Smaller bullet size
        self.image = pg.transform.scale(self.image, (32, 32))  # Mob bullet color
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.direction = direction
        if self.direction.x < 0:
            self.image = pg.transform.flip(self.original_image, True, False)

    def update(self):
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        if (self.rect.right < 0 or self.rect.left > self.game.map.width or self.rect.bottom < 0 or self.rect.top > self.game.map.height):  
            self.kill()
        if self.rect.colliderect(self.game.player.rect):
            self.game.player.take_damage(10)  # Deal 10 damage to the player
            self.kill()

class Wall(Sprite):
    def __init__(self, game, x, y, wall_color):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(wall_color)
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
        self.image = pg.image.load("images/bullet.gif")  # Bullet size
        self.image = pg.transform.scale(self.image, (32,32))  # Bullet color
        self.original_image = self.image
        self.rect = self.image.get_rect() # gets the area of the bullet. which is used for collision
        self.rect.center = (x, y) # sets the inital position of the bullet
        self.speed = 10 # Bullet speed
        self.direction = direction.normalize() # defines the direction the bullet will move in 
        if self.direction.x < 0:
            self.image = pg.transform.flip(self.original_image, True, False)


    def update(self):
        self.rect.x += self.speed * self.direction.x # updates the bullets position based on speed and direction
        self.rect.y += self.speed * self.direction.y 

        if not (0 <= self.rect.x <= self.game.map.width and 0 <= self.rect.y <= self.game.map.height):
            self.kill()

    def draw(self):
        # We don't change bullet position here, just render it relative to the camera
        self.game.camera.apply(self)  # Apply camera offset for drawing
        self.game.screen.blit(self.image, self.rect)

class Camera:
    #defines height and width
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        # determines the width and height of camera
        self.width = width
        self.height = height

    def apply(self, sprite):
        #offsets sprites depending on camera position
        return sprite.rect.move(-self.camera.x, -self.camera.y)
    
    def update(self, player):
        #places player in center of camera and clamps camera position between 0 and height and width
        self.camera.x = player.rect.centerx - WIDTH // 2
        self.camera.y = player.rect.centery - HEIGHT // 2
        self.camera.y = max(0, min(self.camera.y, self.height - HEIGHT))
        self.camera.x = max(0, min(self.camera.x, self.width - WIDTH))

class Map:
    def __init__(self, filename):
        self.data = []
        try:
            with open(filename, 'rt') as f:
                for line in f:
                    self.data.append(line.strip())
        except FileNotFoundError:
            print(f"Error: Map file '{filename}' not found!")
            raise
        except Exception as e:
            print(f"Error loading map file: {e}")
            raise

        if not self.data:
            raise ValueError("Map file is empty or improperly formatted!")

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class DamagingFloor(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(pg.Color('green'))  
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.last_damage_time = 0
    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            now = pg.time.get_ticks()
            # Apply damage only once every 500ms (adjust this value as needed)
            if now - self.last_damage_time > 500:
                self.game.player.take_damage(100)  # Damage the player
                self.last_damage_time = now  # Update the last damage time

class SpikeTrap(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("images/spike.gif")
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            now = pg.time.get_ticks()
            if now - self.game.player.last_hit_time > 1000:  # Damage once per second
                self.game.player.take_damage(10)
                self.game.player.last_hit_time = now


class MovingPlatform(Sprite):
    def __init__(self, game, x, y, dx=2, dy=0):
        self._layer = 1
        self.groups = game.all_sprites, game.all_walls # Added to sprite groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Platform size
        self.image.fill(pg.Color('grey'))  # Platform color
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE  # Convert tile position to screen position
        self.rect.y = y * TILESIZE
        self.dx = dx  # Horizontal movement speed
        self.dy = dy  # Vertical movement speed
        self.original_x = self.rect.x  # Starting X position
        self.original_y = self.rect.y  # Starting Y position
        self.time = 0  # For managing the movement timing

        
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Bounce the platform when it hits the edges of the screen (or map bounds)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy = -self.dy
        # Apply platform movement to player if standing on the platform
        for sprite in self.game.all_sprites:
            if isinstance(sprite, Player) and self.rect.colliderect(sprite.rect):
                sprite.rect.x += self.dx
                sprite.rect.y += self.dy
        
class Portal(Sprite):
    def __init__(self, game, x, y, target_level):
        self.groups = game.all_sprites, game.all_portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(pg.Color('purple'))  # Portal color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)
        self.target_level = target_level

    def update(self):
        pass