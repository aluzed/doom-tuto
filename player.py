from settings import *
import pygame, math

class Player: 
  def __init__(self, game):
    self.game = game
    self.x, self.y = PLAYER_POSITION
    self.angle = PLAYER_ANGLE

  def movement(self):
    sin_a = math.sin(self.angle)
    cos_a = math.cos(self.angle)
    dx, dy = 0, 0

    # the player speed should be relative to the game speed
    speed = PLAYER_SPEED * self.game.delta_time 
    speed_sin = speed * sin_a
    speed_cos = speed * cos_a

    keys = pygame.key.get_pressed()
    # \
    #  °
    if keys[pygame.K_z]:
      dx += speed_cos
      dy += speed_sin
    #  °
    # /
    if keys[pygame.K_s]:
      dx += -speed_cos
      dy += -speed_sin
    # °
    #  \
    if keys[pygame.K_q]:
      dx += speed_sin
      dy += -speed_cos
    #  /
    # °
    if keys[pygame.K_d]:
      dx += -speed_sin
      dy += speed_cos

    # check if we move our player or not
    self.check_wall_collision(dx, dy)

    if keys[pygame.K_LEFT]:
      self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
    if keys[pygame.K_RIGHT]:
      self.angle += PLAYER_ROT_SPEED * self.game.delta_time

    # tau = 2 * pi
    self.angle %= math.tau

  def check_wall(self, x, y):
    return (x, y) not in self.game.map.world_map
  
  def check_wall_collision(self, dx, dy):
    scale = PLAYER_SIZE_SCALE / self.game.delta_time

    # check if next values gonna hit the wall
    if self.check_wall(int(self.x + dx * scale), int(self.y)):
      self.x += dx
    if self.check_wall(int(self.x), int(self.y + dy * scale)):
      self.y += dy

  def draw(self):
    # vision
    if DEBUG_PLAYER_VISION is True:
      pygame.draw.line(self.game.screen, 'yellow', (self.x * MAP_COEFF, self.y * MAP_COEFF), 
                  (
                    self.x * MAP_COEFF + WIDTH * math.cos(self.angle), 
                    self.y * MAP_COEFF + WIDTH * math.sin(self.angle)
                  ), 2)

    # player
    pygame.draw.circle(self.game.screen, 'green', (self.x * MAP_COEFF, self.y * MAP_COEFF), 15)

  def update(self):
    self.movement()
  
  @property
  def pos(self):
    return self.x, self.y 
  
  @property
  def map_pos(self):
    return int(self.x), int(self.y)