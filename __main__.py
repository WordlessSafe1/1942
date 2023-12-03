import pygame
from pygame.locals import *
from spritesheet import SpriteSheet
from random import randint, seed
from typing import Optional


GAME_OVER  = pygame.USEREVENT + 0

DEATH_SCREEN_TICKS = 500

seed("1942")

white = (255, 255, 255)
black = (  0,   0,   0)
red   = (255,   0,   0)
green = (  0, 255,   0)
grey  = ( 31,  31,  31)

SCREEN_SCALE = 2
SCROLL_SPEED = 1

screenheight = 400 * SCREEN_SCALE
screenwidth  = 200 * SCREEN_SCALE

pygame.init()

SMALL_FONT = pygame.font.Font("resources/fnt/1942.ttf", 5 * SCREEN_SCALE)
MEDIUM_FONT = pygame.font.Font("resources/fnt/1942.ttf", 10 * SCREEN_SCALE)
LARGE_FONT = pygame.font.Font("resources/fnt/1942.ttf", int(17.5 * SCREEN_SCALE))

screen = pygame.display.set_mode([screenwidth, screenheight], pygame.SCALED | pygame.RESIZABLE, vsync=1)
clock = pygame.time.Clock()

live_sprites = pygame.sprite.Group()
friendly_sprites = pygame.sprite.Group()
hostile_sprites = pygame.sprite.Group()
friendly_fire = pygame.sprite.Group()

BGM = pygame.mixer.Sound("resources/sfx/StageTheme.wav")
GAME_OVER_MUSIC = pygame.mixer.Sound("resources/sfx/GameOver.wav")
EXPLOSION_SOUND = pygame.mixer.Sound("resources/sfx/Explosion.wav")
FIZZLE_SOUND = pygame.mixer.Sound("resources/sfx/Fizzle.wav")
score = 0
player:Optional["Player"] = None

SPRITESHEET = pygame.image.load("resources/img/Sprites.png").convert()
LOGO = SPRITESHEET.subsurface(pygame.Rect(68, 704, 184, 49))
LOGO = pygame.transform.scale(LOGO, (LOGO.get_width() * (SCREEN_SCALE / 1.5), LOGO.get_height() * (SCREEN_SCALE / 1.5)))
PLAYER_SPRITESHEET = SpriteSheet("resources/img/Sprites.png", 8, 2, pygame.Rect(2, 0, 255, 50))
MAP_SPRITESHEET = pygame.image.load("resources/img/MapTiles.png").convert()

EXPLOSION_SPRITESHEET = SpriteSheet("resources/img/Explosion.png", 6, 1)
EXPLOSION_IMAGES = EXPLOSION_SPRITESHEET.load_strip(0, 6)
for i in range(len(EXPLOSION_IMAGES)):
    EXPLOSION_IMAGES[i] = pygame.transform.scale(EXPLOSION_IMAGES[i], (EXPLOSION_IMAGES[i].get_width() * SCREEN_SCALE, EXPLOSION_IMAGES[i].get_height() * SCREEN_SCALE))
del EXPLOSION_SPRITESHEET

PLAYER_EXPLOSION_SPRITESHEET = SpriteSheet("resources/img/PlayerExplosion.png", 6, 1)
PLAYER_EXPLOSION_IMAGES = PLAYER_EXPLOSION_SPRITESHEET.load_strip(0, 6)
for i in range(len(PLAYER_EXPLOSION_IMAGES)):
    PLAYER_EXPLOSION_IMAGES[i] = pygame.transform.scale(PLAYER_EXPLOSION_IMAGES[i], (PLAYER_EXPLOSION_IMAGES[i].get_width() * SCREEN_SCALE, PLAYER_EXPLOSION_IMAGES[i].get_height() * SCREEN_SCALE))
del PLAYER_EXPLOSION_SPRITESHEET

bullet_sprites = {
    "enemy":  SPRITESHEET.subsurface(pygame.Rect( 74,  89,   6,   6)),
    "player": SPRITESHEET.subsurface(pygame.Rect(101,  82,  15,  14)),
}

for k in bullet_sprites.keys():
    bullet_sprites[k] = pygame.transform.scale(bullet_sprites[k], (bullet_sprites[k].get_width() * SCREEN_SCALE, bullet_sprites[k].get_height() * SCREEN_SCALE))

ocean_raw = MAP_SPRITESHEET.subsurface(pygame.Rect(0, 0, 225, 175))
ocean = pygame.surface.Surface((255, 500))
height = ocean_raw.get_height()
for i in range(4):
    ocean.blit(ocean_raw, (0, height * i))

del ocean_raw

MAP_TILES = [
    ocean,                                                      # Ocean
    MAP_SPRITESHEET.subsurface(pygame.Rect(0,   0, 225,  502)), # Carrier
    MAP_SPRITESHEET.subsurface(pygame.Rect(0, 620, 225, 1428)), # Forest 1
]

GAME_MAP = [
    0, # Ocean
    1, # Carrier
    0, # Ocean
    0, # Ocean
    0, # Ocean
    2, # Forest 1
    0, # Ocean
    1, # Carrier
]

ENEMY_SPRITES = SpriteSheet.from_size("resources/img/Enemies.png", 15, 16, 4, 4)
for y in range(len(ENEMY_SPRITES)):
    for x in range(len(ENEMY_SPRITES[y])):
        sprite = ENEMY_SPRITES[y][x]
        ENEMY_SPRITES[y][x] = pygame.transform.scale(sprite, (sprite.get_width() * SCREEN_SCALE, sprite.get_height() * SCREEN_SCALE))

ENEMY_SIZE = (15 * SCREEN_SCALE, 16 * SCREEN_SCALE)

# 0: dx, 1: dy, 2: ticks, 3: frame_x, 4: frame_y
ENEMY_PATHS = {
    "cross left":  [
        (  -.4,     3,  200,  0, 2),
        (  -.4,     1,   20,  8, 2),
        (  -.4,     0,   20,  9, 2),
        (  -.4,    -1,   20, 10, 2),
        (  -.4,    -3, 2000,  4, 0),
    ],
    "cross left wide":  [
        (  -.7,     3,  200,  0, 2),
        (  -.7,     1,   20,  8, 2),
        (  -.7,     0,   20,  9, 2),
        (  -.7,    -1,   20, 10, 2),
        (  -.7,    -3, 2000,  4, 0),
    ],
    "cross right": [
        (   .4,     3,  200,  0, 2),
        (   .4,     1,   20,  8, 2),
        (   .4,     0,   20,  9, 2),
        (   .4,    -1,   20, 10, 2),
        (   .4,    -3, 2000,  4, 0),
    ],
    "cross right wide": [
        (   .7,     3,  200,  0, 2),
        (   .7,     1,   20,  8, 2),
        (   .7,     0,   20,  9, 2),
        (   .7,    -1,   20, 10, 2),
        (   .7,    -3, 2000,  4, 0),
    ],
    "loop right": [
        (    3,     0,  110,  0, 3),
        ( 2.25,  0.75,   10, 10, 4),
        ( 1.50,  1.50,   10,  9, 4),
        ( 0.75,  2.25,   10,  8, 4),
        (    0,     3,   10,  0, 2),
        (-0.75,  2.25,   10,  6, 4),
        (-1.50,  1.50,   10,  5, 4),
        (-2.25,  0.75,   10,  4, 4),
        (   -3,     0,   10,  0, 1),
        (-2.25, -0.75,   10,  2, 4),
        (-1.50, -1.50,   10,  1, 4),
        (-0.75, -2.25,   10,  0, 4),
        (    0,    -3,   10,  0, 0),
        ( 0.75, -2.25,   10, 14, 4),
        ( 1.50, -1.50,   10, 13, 4),
        ( 2.25, -0.75,   10, 12, 4),
        (    3,     0, 2000,  0, 3),
    ],
    "loop left": [
        (   -3,     0,  110,  0, 1),
        (-2.25,  0.75,   10,  4, 4),
        (-1.50,  1.50,   10,  5, 4),
        (-0.75,  2.25,   10,  6, 4),
        (    0,     3,   10,  0, 2),
        ( 0.75,  2.25,   10,  8, 4),
        ( 1.50,  1.50,   10,  9, 4),
        ( 2.25,  0.75,   10, 10, 4),
        (    3,     0,   10,  0, 3),
        ( 2.25, -0.75,   10, 12, 4),
        ( 1.50, -1.50,   10, 13, 4),
        ( 0.75, -2.25,   10, 14, 4),
        (    0,    -3,   10,  0, 0),
        (-0.75, -2.25,   10,  0, 4),
        (-1.50, -1.50,   10,  1, 4),
        (-2.25, -0.75,   10,  2, 4),
        (   -3,     0, 2000,  0, 1),
    ],
    "loop right double": [
        (    3,     0,   50,  0, 3),
        ( 2.25,  0.75,   10, 10, 4),
        ( 1.50,  1.50,   10,  9, 4),
        ( 0.75,  2.25,   10,  8, 4),
        (    0,     3,   10,  0, 2),
        (-0.75,  2.25,   10,  6, 4),
        (-1.50,  1.50,   10,  5, 4),
        (-2.25,  0.75,   10,  4, 4),
        (   -3,     0,   10,  0, 1),
        (-2.25, -0.75,   10,  2, 4),
        (-1.50, -1.50,   10,  1, 4),
        (-0.75, -2.25,   10,  0, 4),
        (    0,    -3,   10,  0, 0),
        ( 0.75, -2.25,   10, 14, 4),
        ( 1.50, -1.50,   10, 13, 4),
        ( 2.25, -0.75,   10, 12, 4),
        (    3,     0,   50,  0, 3),
        ( 2.25,  0.75,   10, 10, 4),
        ( 1.50,  1.50,   10,  9, 4),
        ( 0.75,  2.25,   10,  8, 4),
        (    0,     3,   10,  0, 2),
        (-0.75,  2.25,   10,  6, 4),
        (-1.50,  1.50,   10,  5, 4),
        (-2.25,  0.75,   10,  4, 4),
        (   -3,     0,   10,  0, 1),
        (-2.25, -0.75,   10,  2, 4),
        (-1.50, -1.50,   10,  1, 4),
        (-0.75, -2.25,   10,  0, 4),
        (    0,    -3,   10,  0, 0),
        ( 0.75, -2.25,   10, 14, 4),
        ( 1.50, -1.50,   10, 13, 4),
        ( 2.25, -0.75,   10, 12, 4),
        (    3,     0, 2000,  0, 3),
    ],

}

for i in range(len(MAP_TILES)):
    tile = MAP_TILES[i]
    MAP_TILES[i] = pygame.transform.scale(tile, (tile.get_width() * SCREEN_SCALE, tile.get_height() * SCREEN_SCALE))

class Player(pygame.sprite.Sprite):
    _L_SPEED = .3                 # Lean speed
    _H_SPEED = 2   * SCREEN_SCALE # Horizontal speed
    _V_SPEED = 2.5 * SCREEN_SCALE # Vertical speed
    _FIRE_COOLDOWN = 6
    _MAX_SHOTS = 3
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._images = PLAYER_SPRITESHEET.load_strip(0, 7)
        self.image = self._images[0]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCREEN_SCALE, self.image.get_height() * SCREEN_SCALE))
        self.rect = pygame.Rect((screenwidth - 62) / 2, screenheight - 75, 62, 50)
        self._anim = 0
        self._frame = 0
        self._tilt_frames = [self._images[6], self._images[4], self._images[2], self._images[0], self._images[1], self._images[3], self._images[5]]
        self._lean = 0
        self._prop_ticks = 0
        self._fire_cooldown = 0

    def update(self, keys):
        collisions = pygame.sprite.spritecollide(self, hostile_sprites, False)
        if collisions:
            for collision in collisions:
                collision.kill()
            self.kill()
            return

        delta_lean = 0
        if self._fire_cooldown:
            self._fire_cooldown -= 1
        if keys[K_RIGHT] and self.rect.x + self.rect.width < screenwidth - 5:
            self.rect.x += self._H_SPEED
            delta_lean += self._L_SPEED
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self._H_SPEED
            delta_lean -= self._L_SPEED
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self._V_SPEED
        if keys[K_DOWN] and self.rect.y + self.rect.height < screenheight:
            self.rect.y += self._V_SPEED
        if keys[K_SPACE] and (not self._fire_cooldown) and len(friendly_fire) < self._MAX_SHOTS:
            bullet = Bullet(self.rect.x + self.rect.width / 2, self.rect.y - 5 * SCREEN_SCALE, "player", 0, 1)
            bullet.rect.x -= bullet.rect.width / 2
            live_sprites.add(bullet)
            friendly_fire.add(bullet)
            self._fire_cooldown = self._FIRE_COOLDOWN
        if not delta_lean and self._lean:
            delta_lean = -self._L_SPEED if self._lean > 0 else self._L_SPEED
        self._lean = max(-3, min(self._lean + delta_lean, 3))

        lean = round(self._lean)
        if lean:
            self.image = self._tilt_frames[lean + 3]
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCREEN_SCALE, self.image.get_height() * SCREEN_SCALE))

        self._prop_ticks += 1
        if not self._prop_ticks % 10:
            self.update_propellers()

    def update_propellers(self):
        prop_up   = (176, 224,   0)
        prop_down = (144, 192,   0)
        for y in range(self.rect.height):
            for x in range(self.rect.width):
                pixel = self.image.get_at((x, y))
                if pixel == prop_up:
                    self.image.set_at((x, y), prop_down)
                elif pixel == prop_down:
                    self.image.set_at((x, y), prop_up)

    def kill(self):
        pygame.event.post(pygame.event.Event(GAME_OVER, {"win": False}))
        explosion = Explosion(self.rect.x, self.rect.y, 1)
        live_sprites.add(explosion)
        super().kill()

    def delete(self):
        super().kill()


class Bullet(pygame.sprite.Sprite):
    _SPEED = 5 * SCREEN_SCALE
    def __init__(self, x, y, style, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        if style not in bullet_sprites.keys():
            raise ValueError(f"Invalid bullet style: {style}")
        self.image = bullet_sprites[style]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._style = style
        self._dx = dx
        self._dy = dy

    def update(self, keys):
        self.rect.y -= self._SPEED * self._dy
        self.rect.x += self._SPEED * self._dx
        if self.rect.y < -self.rect.height:
            self.kill()
            return
        targets = friendly_sprites if self._style == "enemy" else hostile_sprites
        collisions = pygame.sprite.spritecollide(self, targets, True)
        for collision in collisions:
            collision.kill()
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x:int|float, y:int|float, motion:list[tuple[int|float,int|float,int,int,int]], skip_frames:int = 0, skip_ticks:int = 0, time_to_fire:int = -1):
        """
        Initialize an Enemy
        @param motion - a list of tuples(dx, dy, ticks, frame_x, frame_y)
        """
        pygame.sprite.Sprite.__init__(self)
        self._motion = motion
        self._motion_index = skip_frames
        self._motion_ticks = skip_ticks
        self._dx, self._dy, _, frame_x, frame_y = self._motion[self._motion_index]
        self.image = ENEMY_SPRITES[frame_x][frame_y]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self._dead = False
        self._fire_ticks = time_to_fire

        # self._prop_ticks = 0

    def update(self, keys):
        if self._motion_ticks >= self._motion[self._motion_index][2]:
            self._motion_ticks = 0
            self._motion_index += 1
            if self._motion_index >= len(self._motion):
                super().kill()
                return
            self._dx, self._dy, _, frame_x, frame_y = self._motion[self._motion_index]
            self.image = ENEMY_SPRITES[frame_x][frame_y]
        self.x += self._dx
        self.y += self._dy
        self.rect.x = self.x
        self.rect.y = self.y
        self._motion_ticks += 1
        self._dead = False

        if not self._fire_ticks:
            # Fire a bullet towards the player's current position
            dx = player.rect.x - self.rect.x
            dy = self.rect.y - player.rect.y
            mag = (dx ** 2 + dy ** 2) ** .5
            mag = max(mag * 2, 2)
            dx /= mag
            dy /= mag
            bullet = Bullet(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height, "enemy", dx, dy)
            bullet.rect.x -= bullet.rect.width / 2
            live_sprites.add(bullet)

        self._fire_ticks -= 1

    def kill(self):
        global score
        super().kill()
        if not self._dead:
            self._dead = True
            score += 50
            explosion = Explosion(self.rect.x, self.rect.y)
            live_sprites.add(explosion)

    def delete(self):
        super().kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x:int|float, y:int|float, type:int = 0):
        """
        Initialize an Explosion
        @param type - 0: Enemy, 1: Player
        """
        pygame.sprite.Sprite.__init__(self)
        if type == 0:
            FIZZLE_SOUND.play()
            self._images = EXPLOSION_IMAGES
        else:
            BGM.stop()
            EXPLOSION_SOUND.play()
            self._images = PLAYER_EXPLOSION_IMAGES
        self.image = self._images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._frame = 0
        self._ticks = 0

    def update(self, keys):
        self._ticks += 1
        if not self._ticks % 5:
            self._frame += 1
            if self._frame >= len(self._images):
                self.kill()
                return
            self.image = self._images[self._frame]


# [ (WaitTime, EnemyType, ConstructorArguments), ... ]
ENEMY_WAVES = [
    #region Right Loop Troupe
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    #endregion Right Loop Troupe
    #region Left Loop Troupe
    # (  0, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],       0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],       0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],       0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],       0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],       0,  0)),
    #endregion Left Loop Troupe
    #region Mixed Loop Troupe
    # (100, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],       0,  0)),
    # (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],       0,  0)),
    # (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],       0,  0)),
    # (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],       0,  0)),
    # (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    # ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],       0,  0)),
    # (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],      0,  0)),
    #endregion Mixed Loop Troupe
    #region Right Loop Double Troupe
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    # ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    #endregion Right Loop Double Troupe

    (  0, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
    ( 20, Enemy, (screenwidth - 4 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
    ( 25, Enemy, (screenwidth - 3 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,   0)),
    ( 20, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right wide"],       0, -25, 160)),

    (325, Enemy, (screenwidth - 2 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross left wide"],        0, -50)),
    ( 50, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0, 400)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0,  95)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),

    (150, Enemy, (screenwidth - 2 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
    ( 20, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
    ( 25, Enemy, (screenwidth - 3.5*ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,   0)),
    ( 20, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right wide"],       0, -25, 160)),

    (500, Enemy, (screenwidth - 2 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross left wide"],        0, -50, 160)),
    ( 50, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0, 400)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),
    (  0, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0,  95)),
    (  0, Enemy, (-ENEMY_SIZE[0],                  -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 110)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0,  95)),
    ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right double"],      0,  0)),

    (500, Enemy, (2.5 * ENEMY_SIZE[0],             -ENEMY_SIZE[1], ENEMY_PATHS["cross left wide"],        0, -50, 42)),
    ( 50, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
    ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0,  15)),
    ( 90, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0, 110)),
    ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0,  73)),
    ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0,  150)),
    ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0)),
    (  0, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
    ( 20, Enemy, (2 * ENEMY_SIZE[0],               -ENEMY_SIZE[1], ENEMY_PATHS["cross right wide"],            0,  25)),
    ( 25, Enemy, (screenwidth - 3 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,   0,  15)),




    (None, None, -1), # Wait infinitely until the game ends
]

def start_game() -> int:
    """
    Start the game loop.
    Return 0 to restart the game, -1 to quit
    """
    global player
    BGM.play(loops=-1)
    pygame.display.set_caption("1942")
    running = True
    player = Player()
    friendly_sprites.add(player)
    live_sprites.add(player)
    map_tile = GAME_MAP[0]
    transfer_map_tile = GAME_MAP[1]
    map_pos  = 200
    transfer_map_pos = map_pos + MAP_TILES[transfer_map_tile].get_height()
    next_map_tile = 2
    wave_ticks = 0
    wave = 0
    paused = False
    game_over = 0
    score_text = SMALL_FONT.render("Score", True, red)
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == GAME_OVER:
                game_over = 1
            elif event.type == KEYDOWN and (not game_over) and event.key == K_ESCAPE:
                if paused:
                    pygame.mixer.unpause()
                    paused = False
                else:
                    pygame.mixer.pause()
                    paused = True
                    text = LARGE_FONT.render("PAUSED", True, red)
                    screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2))
                    pygame.display.flip()

        if paused:
            continue


        keys = pygame.key.get_pressed()
        live_sprites.update(keys)


        #region SpawnEnemies
        while wave_ticks == ENEMY_WAVES[wave][0]:
            _, type, args = ENEMY_WAVES[wave]
            enemy = type(*args)
            hostile_sprites.add(enemy)
            live_sprites.add(enemy)
            wave_ticks = 0
            wave += 1
        wave_ticks += 1
        #endregion SpawnEnemies

        #region MapScrolling
        if map_pos <= 0:
            if next_map_tile >= len(GAME_MAP):
                # Do a proper end game, you win, blah blah blah
                return 0
            map_tile, transfer_map_tile = transfer_map_tile, GAME_MAP[next_map_tile]
            next_map_tile += 1
            map_pos = transfer_map_pos
            transfer_map_pos = map_pos + MAP_TILES[transfer_map_tile].get_height()
        map_pos -= SCROLL_SPEED
        transfer_map_pos -= SCROLL_SPEED
        #endregion MapScrolling


        #region Draw
        screen.fill(grey)

        screen.blit(MAP_TILES[map_tile], (0, screenheight - map_pos))
        screen.blit(MAP_TILES[transfer_map_tile], (0, screenheight - transfer_map_pos))

        # pygame.draw.rect(screen, red, player.rect, 1)
        live_sprites.draw(screen)

        screen.blit(score_text, ((screenwidth - score_text.get_width()) / 2, 5 * SCREEN_SCALE))
        text = SMALL_FONT.render(str(score), True, white)
        screen.blit(text, ((screenwidth - text.get_width()) / 2, score_text.get_height() + 7 * SCREEN_SCALE))

        if game_over:
            game_over += 1
            if game_over > DEATH_SCREEN_TICKS:
                return 0
            if game_over > DEATH_SCREEN_TICKS // 8:
                text = LARGE_FONT.render("GAME OVER", True, red)
                screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2))
            elif game_over == DEATH_SCREEN_TICKS // 8:
                GAME_OVER_MUSIC.play()


        pygame.display.flip()
        #endregion Draw

        clock.tick(60)
    return -1

def cleanup() -> None:
    global score
    seed("1942")
    for sprite in live_sprites.sprites():
        (sprite.delete or sprite.kill)()
    screen.fill(black)
    pygame.display.flip()
    score = 0

def main_menu() -> bool:
    global screen, clock
    pygame.display.set_caption("1942")
    running = True
    ticks = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return True

        screen.fill(black)
        screen.blit(LOGO, ((screenwidth - LOGO.get_width()) / 2, screenheight / 2 - LOGO.get_height()))
        text = SMALL_FONT.render("Press Enter to Start", True, white)
        screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2 + 2 * text.get_height()))
        pygame.display.flip()
        clock.tick(60)

def main() -> None:
    if not main_menu():
        return
    while not start_game():
        cleanup()
        if not main_menu(): 
            break
    pygame.quit()
    return




if __name__ == "__main__":
    main()
