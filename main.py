# this file was created by: Brayden Ho

# this is where we import libraries and modules
import random
import pygame as pg
from settings import *
# from sprites import *
from sprites_side_scroller import *
from tilemap import *
from os import path
# we are editing this file after installing git

'''

Design Goals: 
make the player and mobs be able to shoot bullets
create health bars for the player and mobs
create a camera that follows the player around the map
extend the level 1 map.

Elevator Pitch: create a slide scroller where a character has a blaster and must blast through the hordes of enemies.
There were be a boss at the end with special powers.

GOALS: To defeat the boss.
RULES:, shoot gun, waves of enemies
FEEDBACK: health bar, enemy health 
FREEDOM: left and right movement, jumping.

What's the sentence: Player 1 shoots bullet at enemy and enemy takes damage...

Alpha Goal: to create a first person shooter with dodging, collision and projectiles

Sources: Coding with Russ(Pygame Scrolling Shooter Game Beginner Tutorial in Python - Part 4-Shooting Bullets):
used to allow player to fire bullets


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
    pg.display.set_caption("Braydens' Coolest Game Ever...")
    self.playing = True
    self.running = True
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    map_file = path.join(self.game_folder, 'level1.txt')
    if not path.exists(map_file):
        raise FileNotFoundError("Map file 'level1.txt' not found!")
    self.map = Map(map_file)

  def new(self):
    self.load_data()
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_bullets = pg.sprite.Group() #adding bullets into main
    # instantiating the class to create the player object 
    # self.player = Player(self, 5, 5)
    # self.mob = Mob(self, 100, 100)
    # self.wall = Wall(self, WIDTH//2, HEIGHT//2)
    # # instantiates wall and mob objects
    # for i in range(12):
    #   Wall(self, TILESIZE*i, HEIGHT/2)
    #   Mob(self, TILESIZE*i, TILESIZE*i)
    # attributes for each sprite
    WALL_COLORS = [pg.Color('grey'), pg.Color('brown'), pg.Color('lightgrey'), pg.Color('darkgrey'), pg.Color('tan')]
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          wall_color = random.choice(WALL_COLORS)
          Wall(self, col, row, wall_color)
        elif tile == 'M':
          Mob(self, col, row)
        elif tile == 'P':
          self.player = Player(self, col, row)
        elif tile == 'U': 
          Powerup(self, col, row)
        elif tile == 'C':
          Coin(self, col, row)

    self.camera = Camera(self.map.width * TILESIZE, self.map.height * TILESIZE) #calcualtes total width and height of map for camera to stay inbounds

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

  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
          self.running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
              self.playing = False
              self.running = False
  # process
  # this is where the game updates the game state
  def update(self):
    self.all_sprites.update()
    self.camera.update(self.player)

  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  # output
  def draw(self):
    # makes the entire screen black and draws all sprites
    self.screen.fill(BLACK)
    for sprite in self.all_sprites:
      #creates each sprite based on camera position
      self.screen.blit(sprite.image, self.camera.apply(sprite))
      # only applies it to Mob
      if isinstance(sprite, Player):
         # makes health bar follow player and mobs
         draw_health_bar(self.screen, sprite.rect.x - self.camera.camera.x, sprite.rect.y - 10 - self.camera.camera.y, sprite.health, sprite.max_health)
      elif isinstance(sprite, Mob): 
        # uses the same code for Mob class
          draw_health_bar(self.screen, sprite.rect.x - self.camera.camera.x, sprite.rect.y - 10 - self.camera.camera.y, sprite.health, sprite.max_health)
    #displays frame rate
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    #displays coin count
    self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
    pg.display.flip()


if __name__ == "__main__":
  # instantiate
  g = Game()
  g.new()
  while g.running:
    g.run()
  pg.quit()
  