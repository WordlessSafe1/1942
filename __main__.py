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

all_sprites = pygame.sprite.Group()

bgm = pygame.mixer.Sound("resources/sfx/StageTheme.wav")
bgm.play(loops=-1)

PLAYER_SPRITESHEET = SpriteSheet("resources/img/Sprites.png", 8, 2, pygame.Rect(0, 0, 255, 50))
MAP_SPRITESHEET = pygame.image.load("resources/img/MapTiles.png").convert()
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

for i in range(len(MAP_TILES)):
    tile = MAP_TILES[i]
    MAP_TILES[i] = pygame.transform.scale(tile, (tile.get_width() * SCREEN_SCALE, tile.get_height() * SCREEN_SCALE))

space_held = False

class Player(pygame.sprite.Sprite):
    _L_SPEED = .3                 # Lean speed
    _H_SPEED = 2   * SCREEN_SCALE # Horizontal speed
    _V_SPEED = 2.5 * SCREEN_SCALE # Vertical speed
    
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

    def update(self, keys):
        global space_held
        delta_lean = 0
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
        if keys[K_SPACE] and not space_held:
            self._frame = (self._frame + 1) % len(self._images)
            self.image = self._images[self._frame]
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCREEN_SCALE, self.image.get_height() * SCREEN_SCALE))
            space_held = True
        elif not keys[K_SPACE]:
            space_held = False
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



def main() -> None:
    pygame.display.set_caption("1942")
    running = True
    player = Player()
    all_sprites.add(player)
    map_tile = GAME_MAP[0]
    transfer_map_tile = GAME_MAP[1]
    map_pos  = 200
    transfer_map_pos = map_pos + MAP_TILES[transfer_map_tile].get_height()
    next_map_tile = 2
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False


        keys = pygame.key.get_pressed()
        player.update(keys)


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
        all_sprites.draw(screen)
        pygame.display.flip()
        #endregion Draw

        clock.tick(60)
    pygame.quit()
    return



if __name__ == "__main__":
    main()