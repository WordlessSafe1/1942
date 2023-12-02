import pygame
from pygame.locals import *
from spritesheet import SpriteSheet

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
screen = pygame.display.set_mode([screenwidth, screenheight], pygame.SCALED, vsync=1)
clock = pygame.time.Clock()

live_sprites = pygame.sprite.Group()
friendly_sprites = pygame.sprite.Group()
hostile_sprites = pygame.sprite.Group()
friendly_fire = pygame.sprite.Group()

bgm = pygame.mixer.Sound("resources/sfx/StageTheme.wav")
bgm.play(loops=-1)

SPRITESHEET = pygame.image.load("resources/img/Sprites.png").convert()
PLAYER_SPRITESHEET = SpriteSheet("resources/img/Sprites.png", 8, 2, pygame.Rect(2, 0, 255, 50))
MAP_SPRITESHEET = pygame.image.load("resources/img/MapTiles.png").convert()
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

# 0: dx, 1: dy, 2: ticks, 3: frame_x, 4: frame_y
ENEMY_PATHS = {
    "cross left":  [ (0,0,0,0,0), # init
        (-.4,  3,  200,  0, 2),
        (-.4,  1,   20,  8, 2),
        (-.4,  0,   20,  9, 2),
        (-.4, -1,   20, 10, 2),
        (-.4, -3, 2000,  4, 0),
    ],
    "cross right": [ (0,0,0,0,0), # init
        ( .4,  3,  200,  0, 2),
        ( .4,  1,   20,  8, 2),
        ( .4,  0,   20,  9, 2),
        ( .4, -1,   20, 10, 2),
        ( .4, -3, 2000,  4, 0),
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
    def __init__(self, x:int|float, y:int|float, motion:list[tuple[int|float,int|float,int,int,int]], skip_frames:int = 0, skip_ticks:int = 0):
        """
        Initialize an Enemy
        @param motion - a list of tuples(dx, dy, ticks, frame_x, frame_y)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = ENEMY_SPRITES[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._motion = motion
        self._motion_index = skip_frames
        self._motion_ticks = skip_ticks
        self._dx = 0
        self._dy = 0
        self.x = x
        self.y = y
        # self._prop_ticks = 0

    def update(self, keys):
        if self._motion_ticks >= self._motion[self._motion_index][2]:
            self._motion_ticks = 0
            self._motion_index += 1
            if self._motion_index >= len(self._motion):
                self.kill()
                return
            self._dx, self._dy, _, frame_x, frame_y = self._motion[self._motion_index]
            self.image = ENEMY_SPRITES[frame_x][frame_y]
        self.x += self._dx
        self.y += self._dy
        self.rect.x = self.x
        self.rect.y = self.y
        self._motion_ticks += 1

        # self._prop_ticks += 1
        # if not self._prop_ticks % 10:
        #     self.update_propellers()
        
    # My trick of flipping the colors doesn't work because there are other parts of the sprite that are the same color
    # def update_propellers(self):
    #     prop_up   = (192, 192, 144)
    #     prop_down = (128, 128,  80)
    #     for y in range(self.rect.height):
    #         for x in range(self.rect.width):
    #             pixel = self.image.get_at((x, y))
    #             if pixel == prop_up:
    #                 self.image.set_at((x, y), prop_down)
    #             elif pixel == prop_down:
    #                 self.image.set_at((x, y), prop_up)


def main() -> None:
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
    enemy = Enemy(0, 0, ENEMY_PATHS["cross left"], 0, 50)
    enemy.y = -enemy.rect.height
    enemy.x = screenwidth - enemy.rect.width
    hostile_sprites.add(enemy)
    live_sprites.add(enemy)
    wave_ticks = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False


        keys = pygame.key.get_pressed()
        live_sprites.update(keys)


        # wave_ticks += 1
        # if not wave_ticks % 100:
        #     enemy = Enemy(screenwidth, -100, ENEMY_PATHS["cross left"])
        #     enemy.rect.y = -enemy.rect.height
        #     hostile_sprites.add(enemy)
        #     live_sprites.add(enemy)
        #     enemy = Enemy(0, -80, ENEMY_PATHS["cross right"])
        #     hostile_sprites.add(enemy)
        #     live_sprites.add(enemy)


        #region Draw
        screen.fill(grey)

        #region MapScrolling
        if map_pos <= 0:
            if next_map_tile >= len(GAME_MAP):
                # Do a proper end game, you win, blah blah blah
                pygame.quit()
                return
            map_tile, transfer_map_tile = transfer_map_tile, GAME_MAP[next_map_tile]
            next_map_tile += 1
            map_pos = transfer_map_pos
            transfer_map_pos = map_pos + MAP_TILES[transfer_map_tile].get_height()
        map_pos -= SCROLL_SPEED
        transfer_map_pos -= SCROLL_SPEED
        screen.blit(MAP_TILES[map_tile], (0, screenheight - map_pos))
        screen.blit(MAP_TILES[transfer_map_tile], (0, screenheight - transfer_map_pos))
        #endregion MapScrolling

        # pygame.draw.rect(screen, red, player.rect, 1)
        live_sprites.draw(screen)
        pygame.display.flip()
        #endregion Draw

        clock.tick(60)
    pygame.quit()
    return



if __name__ == "__main__":
    main()