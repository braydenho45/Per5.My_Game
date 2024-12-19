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

Sources: 
1. Coding with Russ(Pygame Scrolling Shooter Game Beginner Tutorial in Python - Part 4-Shooting Bullets):
used to allow player to fire bullets

2. How to make a menu screen in pygame by baraltech: used to create main menu screen for game

3. Learn pygame! #6 Game over screen: used to create a game over screen

4. Projectiles and Enemy Behavior in pygame! Python Game Development Tutorial # 3: used to allow mobs to shoot bullets back at player and chase player.

5. Paul Baumgarten Pygame 12 Portals: used to help make a portal that teleports player between levels

6. Coding with Russ How to create Health Bars Pygame tutorials: used to make health bars for player and mobs

7. Chatgpt: Prompt was "how to insert images over the player, mobs, and objects in pygame in Visual Studio Code?"

8. CDcodes Pygame Camera Tutorial: How to make a Side-Scrolling Camera system: used to make camera that follows player movements

Design Goals: 
make the player and mobs be able to shoot bullets
create health bars for the player and mobs
create a camera that follows the player around the map
extend the level 1 map 
have a bossfight at the end of the level

Elevator Pitch: create a slide scroller where a character has a blaster and must blast through the hordes of enemies and platform across dangerous territory.
There were be a boss at the end with special powers.

GOALS: To defeat the boss.
RULES:, shoot gun, waves of enemies
FEEDBACK: health bar, enemy health 
FREEDOM: left and right movement, jumping.

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
    pg.display.set_caption("Braydens' Coolest Game Ever...")
    self.playing = True
    self.running = True
    self.score = 0
    self.level_file = 'level1.txt'
 
  def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

  #code for main menu screen
  def main_menu(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Bullet Dash", 48, RED, WIDTH // 2, HEIGHT // 4)
        self.draw_text(self.screen, "Press S to Start", 32, WHITE, WIDTH // 2, HEIGHT // 2)
        self.draw_text(self.screen, "Press C for Controls", 32, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
        self.draw_text(self.screen, "Press Q to Quit", 32, WHITE, WIDTH // 2, HEIGHT // 2 + 100)

        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        waiting = False  # Start the game
                        self.new()
                        self.run()
                    elif event.key == pg.K_c:
                        self.instructions_screen()
                    elif event.key == pg.K_q:
                        self.running = False
                        waiting = False

  def instructions_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Controls", 48, WHITE, WIDTH // 2, HEIGHT // 4)
        self.draw_text(self.screen, "Move with A and D, Jump with SPACE", 24, WHITE, WIDTH // 2, HEIGHT // 2)
        self.draw_text(self.screen, "Shoot bullets with F", 24, WHITE, WIDTH // 2, HEIGHT // 2 + 40)
        self.draw_text(self.screen, "Press M to return to Menu", 24, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        self.draw_text(self.screen, "Goal: Kill enemies and reach end of level to progress", 24, WHITE, WIDTH // 2, HEIGHT // 2 + 120)
        pg.display.flip()

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_m:
                        waiting = False
                        self.main_menu()

  
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    # with open(path.join(self.game_folder, HS_FILE), 'w') as f:
      # f.write(str(0))
    try:
      with open(path.join(self.game_folder, HS_FILE), 'r') as f:
            self.highscore = int(f.read())
    except:
       with open(path.join(self.game_folder, HS_FILE), 'w') as f:
            f.write(str(self.highscore)) 
    self.load_level(self.level_file)

  def load_level(self, level_file):
    # Clear existing sprites
     self.all_sprites.empty()
     self.all_walls.empty()
     self.all_portals.empty()
     self.all_coins.empty()
     self.all_powerups.empty()
     self.all_bullets.empty()
     self.mobs.empty()

     map_file = path.join(self.game_folder, level_file)
     if not path.exists(map_file):
        raise FileNotFoundError(f"Map file '{level_file}' not found!")
     self.map = Map(map_file)

     for row, tiles in enumerate(self.map.data):
        for col, tile in enumerate(tiles):
            if tile == '1':
                wall_color = random.choice([pg.Color('grey'), pg.Color('brown'), pg.Color('lightgrey')])
                Wall(self, col, row, wall_color)
            elif tile == 'P':
                Portal(self, col, row, "level2.txt")  # Change to load the next level, if needed
            elif tile == 'M':
                Mob(self, col, row)
            elif tile == 'X':
                self.player = Player(self, col, row)  # Reinitialize the player at the start of the new level
            elif tile == 'U':
                Powerup(self, col, row)
            elif tile == 'C':
                Coin(self, col, row)
            elif tile == 'D':
                DamagingFloor(self, col, row)
            elif tile == 'S':
                SpikeTrap(self, col, row)
            elif tile == 'L':
                MovingPlatform(self, col, row, dx=2, dy=0)

    # Adjust camera bounds for the new level
        self.camera = Camera(self.map.width * TILESIZE, self.map.height * TILESIZE)


  def new(self):
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_bullets = pg.sprite.Group() #adding bullets into main
    self.mobs = pg.sprite.Group()
    self.all_portals = pg.sprite.Group()
    self.load_data()
    # attributes for each sprite
    WALL_COLORS = [pg.Color('grey'), pg.Color('brown'), pg.Color('lightgrey'), pg.Color('darkgrey'), pg.Color('tan')]
    self.player = None
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          wall_color = random.choice(WALL_COLORS)
          Wall(self, col, row, wall_color)
        elif tile == 'P':
                Portal(self, col, row, "level2.txt")
        elif tile == 'M':
          Mob(self, col, row)
        elif tile == 'X':
          self.player = Player(self, col, row)
        elif tile == 'U': 
          Powerup(self, col, row)
        elif tile == 'C':
          Coin(self, col, row)
        elif tile == 'D':  # Damaging Floor
            DamagingFloor(self, col, row)
        elif tile == 'S':  # Spike Trap
            SpikeTrap(self, col, row)
        elif tile == 'L':  # Moving Platform
            MovingPlatform(self, col, row, dx=2, dy=0)

    if self.player is None:
      raise ValueError("Player spawn point (X) not found in the map!") 

    self.camera = Camera(self.map.width * TILESIZE, self.map.height * TILESIZE) #calcualtes total width and height of map for camera to stay inbounds

# this is a method
# methods are like functions that are part of a class
# the run method runs the game loop
  def run(self):
      self.playing = True
      while self.playing:
        self.dt = self.clock.tick(FPS) / 1000
        self.events()
        self.update()
        self.draw()
        if self.player.health <= 0:
          self.playing = False
          self.game_over_screen()

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

    portal_hits = pg.sprite.spritecollide(self.player, self.all_portals, False)
    if portal_hits:
        portal = portal_hits[0]
        self.level_file = portal.target_level  # Load the next level
        self.load_level(self.level_file)
        self.new()  # Re-initialize the game with the new level

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

  def game_over_screen(self):
    self.screen.fill(BLACK)
    self.draw_text(self.screen, "GAME OVER", 64, RED, WIDTH // 2, HEIGHT // 4)
    self.draw_text(self.screen, "Press R to Restart", 32, WHITE, WIDTH // 2, HEIGHT // 2)
    self.draw_text(self.screen, "Press M for Main Menu", 32, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    self.draw_text(self.screen, "Press Q to Quit", 32, WHITE, WIDTH // 2, HEIGHT // 2 + 100)
    pg.display.flip()
    waiting = True
    while waiting:
      for event in pg.event.get():
        if event.type == pg.QUIT:
            self.running = False
            waiting = False
        elif event.type == pg.KEYDOWN:
          if event.key == pg.K_r:
              self.playing = True
              self.new()  # Start a new game
              self.run()
              waiting = False
          elif event.key == pg.K_m:  # Return to menu
              self.main_menu()
              ccwaiting = False
          elif event.key == pg.K_q:
              self.running = False
              waiting = False


if __name__ == "__main__":
  # instantiate
  g = Game()
  g.main_menu()
  while g.running:
      g.new()
      g.run()
  pg.quit()
  