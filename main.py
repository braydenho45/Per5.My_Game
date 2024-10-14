# this file was created by: Brayden Ho

# this file was created by: Chris Cozort

# this is where we import libraries and modules
import pygame as pg
from settings import *
# from sprites import *
from sprites_side_scroller import *
from tilemap import *
from os import path
# we are editing this file after installing git

'''
Elevator Pitch: create a slide scroller where a character has a blaster and must blast through the hordes of enemies.
There were be a boss at the end with special powers.

GOALS: To defeat the boss.
RULES:, shoot gun, roll, waves of enemies
FEEDBACK: health bar, enemy health, 
FREEDOM: left and right movement, dodging. 

What's the sentence: Player 1 shoots bullet at enemy and enemy takes damage...

Alpha Goal: to create a first person shooter with dodging, collision and projectiles

'''

# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    # sound mixer...
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chris' Coolest Game Ever...")
    self.playing = True
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'level1.txt'))
  def new(self):
    self.load_data()
    print(self.map.data)
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_camera = pg
    # instantiating the class to create the player object 
    # self.player = Player(self, 5, 5)
    # self.mob = Mob(self, 100, 100)
    # self.wall = Wall(self, WIDTH//2, HEIGHT//2)
    # # instantiates wall and mob objects
    # for i in range(12):
    #   Wall(self, TILESIZE*i, HEIGHT/2)
    #   Mob(self, TILESIZE*i, TILESIZE*i)
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'U':
          Powerup(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
    for i in range(1000):
      Powerup(self, randint(0,WIDTH), randint(0,HEIGHT))

# this is a method
# methods are like functions that are part of a class
# the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()

    pg.quit()
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites...and I MEAN ALL OF THEM
    self.camera.update(self.player)
    self.all_sprites.update()
    if self.player.vel.x > 0:
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.rect.x -= self.player.speed
    if len([wall for wall in self.all_walls if wall.rect.right > WIDTH]) == 0:
        self.spawn_new_wall()
    if self.player.vel.x < 0:
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.rect.x -= self.player.speed
    if len([wall for wall in self.all_walls if wall.rect.right > WIDTH]) == 0:
        self.spawn_new_wall()
    for wall in self.all_walls:
        if wall.rect.right < 0:  
            wall.kill()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  # output
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
    pg.display.flip()
    for sprite in self.all_sprites:
       self.screen.blit(sprite.image, self.camera.apply(sprite))
       self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
       pg.display.flip()

  def spawn_new_wall(self):
    new_wall_x = WIDTH + TILESIZE 
    new_wall_y = randint(0, HEIGHT // TILESIZE) * TILESIZE
    Wall(self, new_wall_x, new_wall_y)
  
  def new(self):
     self.load_data()
     self.camera = Camera(self.map.width, self.map.height)
    
if __name__ == "__main__":
  # instantiate
  print("main is running...")
  g = Game()
  print("main is running...")
  g.new()
  g.run()
  