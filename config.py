import pygame
from pygame.locals import *
from spritesheet import SpriteSheet

GAME_OVER  = pygame.USEREVENT + 0

DEATH_SCREEN_TICKS = 500

white = (255, 255, 255)
black = (  0,   0,   0)
red   = (255,   0,   0)
green = (  0, 255,   0)
grey  = ( 31,  31,  31)

SCREEN_SCALE = 2
SCROLL_SPEED = 1

screenheight = 400 * SCREEN_SCALE
screenwidth  = 200 * SCREEN_SCALE

TINY_FONT:   pygame.font.Font = None
SMALL_FONT:  pygame.font.Font = None
MEDIUM_FONT: pygame.font.Font = None
LARGE_FONT:  pygame.font.Font = None

screen: pygame.Surface    = None
clock:  pygame.time.Clock = None

live_sprites:       pygame.sprite.Group = None
friendly_sprites:   pygame.sprite.Group = None
hostile_sprites:    pygame.sprite.Group = None
friendly_fire:      pygame.sprite.Group = None

BGM:                pygame.mixer.Sound = None
GAME_OVER_MUSIC:    pygame.mixer.Sound = None
WIN_MUSIC:          pygame.mixer.Sound = None
EXPLOSION_SOUND:    pygame.mixer.Sound = None
FIZZLE_SOUND:       pygame.mixer.Sound = None

SPRITESHEET = None
LOGO        = None
LOGO        = None

bullet_sprites = None

PLAYER_SPRITESHEET  = None
MAP_SPRITESHEET     = None

EXPLOSION_IMAGES        = None
PLAYER_EXPLOSION_IMAGES = None

MAP_TILES:      list[pygame.Surface]        = None
ENEMY_SPRITES:  list[list[pygame.Surface]]  = None

ENEMY_SIZE = (15 * SCREEN_SCALE, 16 * SCREEN_SCALE)

player = None
score: int = 0

CONTROLS = {
    "arrows":   [K_UP, K_LEFT, K_DOWN, K_RIGHT, K_SPACE],
    "wasd":     [K_w, K_a, K_s, K_d, K_SPACE],
    "vim":      [K_k, K_h, K_j, K_l, K_SPACE],
}

control_scheme = "wasd"


def init():
    global screen, clock, TINY_FONT, SMALL_FONT, MEDIUM_FONT, LARGE_FONT
    screen = pygame.display.set_mode([screenwidth, screenheight], pygame.SCALED | pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    TINY_FONT = pygame.font.Font("resources/fnt/1942.ttf", int(3.5 * SCREEN_SCALE))
    SMALL_FONT = pygame.font.Font("resources/fnt/1942.ttf", 5 * SCREEN_SCALE)
    MEDIUM_FONT = pygame.font.Font("resources/fnt/1942.ttf", 10 * SCREEN_SCALE)
    LARGE_FONT = pygame.font.Font("resources/fnt/1942.ttf", int(17.5 * SCREEN_SCALE))

    global live_sprites, friendly_sprites, hostile_sprites, friendly_fire
    live_sprites = pygame.sprite.Group()
    friendly_sprites = pygame.sprite.Group()
    hostile_sprites = pygame.sprite.Group()
    friendly_fire = pygame.sprite.Group()

    global BGM, GAME_OVER_MUSIC, WIN_MUSIC, EXPLOSION_SOUND, FIZZLE_SOUND
    BGM = pygame.mixer.Sound("resources/sfx/StageTheme.wav")
    GAME_OVER_MUSIC = pygame.mixer.Sound("resources/sfx/GameOver.wav")
    WIN_MUSIC = pygame.mixer.Sound("resources/sfx/RankTheme1.wav")
    EXPLOSION_SOUND = pygame.mixer.Sound("resources/sfx/Explosion.wav")
    FIZZLE_SOUND = pygame.mixer.Sound("resources/sfx/Fizzle.wav")

    global SPRITESHEET, LOGO
    SPRITESHEET = pygame.image.load("resources/img/Sprites.png").convert()
    LOGO = SPRITESHEET.subsurface(pygame.Rect(68, 704, 184, 49))
    LOGO = pygame.transform.scale(LOGO, (LOGO.get_width() * (SCREEN_SCALE / 1.5), LOGO.get_height() * (SCREEN_SCALE / 1.5)))

    global bullet_sprites
    bullet_sprites =  {
        "enemy":  SPRITESHEET.subsurface(pygame.Rect( 74,  89,   6,   6)),
        "player": SPRITESHEET.subsurface(pygame.Rect(101,  82,  15,  14)),
    }
    for k in bullet_sprites.keys():
        bullet_sprites[k] = pygame.transform.scale(bullet_sprites[k], (bullet_sprites[k].get_width() * SCREEN_SCALE, bullet_sprites[k].get_height() * SCREEN_SCALE))

    global PLAYER_SPRITESHEET, MAP_SPRITESHEET
    PLAYER_SPRITESHEET = SpriteSheet("resources/img/Sprites.png", 8, 2, pygame.Rect(2, 0, 255, 50))
    MAP_SPRITESHEET = pygame.image.load("resources/img/MapTiles.png").convert()

    global EXPLOSION_IMAGES, PLAYER_EXPLOSION_IMAGES
    EXPLOSION_SPRITESHEET = SpriteSheet("resources/img/Explosion.png", 6, 1)
    EXPLOSION_IMAGES = EXPLOSION_SPRITESHEET.load_strip(0, 6)
    for i in range(len(EXPLOSION_IMAGES)):
        EXPLOSION_IMAGES[i] = pygame.transform.scale(EXPLOSION_IMAGES[i], (EXPLOSION_IMAGES[i].get_width() * SCREEN_SCALE, EXPLOSION_IMAGES[i].get_height() * SCREEN_SCALE))
    PLAYER_EXPLOSION_SPRITESHEET = SpriteSheet("resources/img/PlayerExplosion.png", 6, 1)
    PLAYER_EXPLOSION_IMAGES = PLAYER_EXPLOSION_SPRITESHEET.load_strip(0, 6)
    for i in range(len(PLAYER_EXPLOSION_IMAGES)):
        PLAYER_EXPLOSION_IMAGES[i] = pygame.transform.scale(PLAYER_EXPLOSION_IMAGES[i], (PLAYER_EXPLOSION_IMAGES[i].get_width() * SCREEN_SCALE, PLAYER_EXPLOSION_IMAGES[i].get_height() * SCREEN_SCALE))

    global MAP_TILES
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
    for i in range(len(MAP_TILES)):
        tile = MAP_TILES[i]
        MAP_TILES[i] = pygame.transform.scale(tile, (tile.get_width() * SCREEN_SCALE, tile.get_height() * SCREEN_SCALE))

    global ENEMY_SPRITES, ENEMY_SIZE
    ENEMY_SPRITES = SpriteSheet.from_size("resources/img/Enemies.png", 15, 16, 4, 4)
    for y in range(len(ENEMY_SPRITES)):
        for x in range(len(ENEMY_SPRITES[y])):
            sprite = ENEMY_SPRITES[y][x]
            ENEMY_SPRITES[y][x] = pygame.transform.scale(sprite, (sprite.get_width() * SCREEN_SCALE, sprite.get_height() * SCREEN_SCALE))
    ENEMY_SIZE = (15 * SCREEN_SCALE, 16 * SCREEN_SCALE)
