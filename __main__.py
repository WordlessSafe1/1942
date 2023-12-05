import pygame
from pygame.locals import *
from spritesheet import SpriteSheet
from random import randint, seed
from typing import Optional
from abc import ABC, abstractmethod
from bullet import Bullet
from config import SCREEN_SCALE
import config as cfg
from config import ENEMY_SIZE, screenheight, screenwidth
from character import Player, Enemy


pygame.init()
cfg.init()


GAME_MAP = [
    0, # Ocean
    1, # Carrier
    0, # Ocean
    # 0, # Ocean
    # 0, # Ocean
    2, # Forest 1
    0, # Ocean
    1, # Carrier
]


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

    (250, Enemy, (-ENEMY_SIZE[0],                screenheight / 3, ENEMY_PATHS["cross right"],            0, 175,  20)),
    ( 10, Enemy, (screenwidth,                   screenheight / 3,  ENEMY_PATHS["cross left"],            0, 170,  10)),
    ( 10, Enemy, (2.5 * ENEMY_SIZE[0],             -ENEMY_SIZE[1], ENEMY_PATHS["cross left wide"],        0, -50,  42)),
    (  5, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
    ( 15, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
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




    (None, None, -1), # Wait infinitely until the game ends
]

def start_game() -> int:
    """
    Start the game loop.
    Return 0 to restart the game, -1 to quit
    """
    cfg.BGM.play(loops=-1)
    pygame.display.set_caption("1942")
    running = True
    cfg.player = Player()
    cfg.friendly_sprites.add(cfg.player)
    cfg.live_sprites.add(cfg.player)
    map_tile = GAME_MAP[0]
    transfer_map_tile = GAME_MAP[1]
    map_pos  = 200
    transfer_map_pos = map_pos + cfg.MAP_TILES[transfer_map_tile].get_height()
    next_map_tile = 2
    wave_ticks = 0
    wave = 0
    paused = False
    game_over = 0
    score_text = cfg.SMALL_FONT.render("Score", True, cfg.red)
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == cfg.GAME_OVER:
                game_over = 1
            elif event.type == KEYDOWN and (not game_over) and event.key == K_ESCAPE:
                if paused:
                    pygame.mixer.unpause()
                    paused = False
                else:
                    pygame.mixer.pause()
                    paused = True
                    text = cfg.LARGE_FONT.render("PAUSED", True, cfg.red)
                    cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2))
                    pygame.display.flip()

        if paused:
            continue


        keys = pygame.key.get_pressed()
        cfg.live_sprites.update(keys)


        #region SpawnEnemies
        while wave_ticks == ENEMY_WAVES[wave][0]:
            _, type, args = ENEMY_WAVES[wave]
            enemy = type(*args)
            cfg.hostile_sprites.add(enemy)
            cfg.live_sprites.add(enemy)
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
            transfer_map_pos = map_pos + cfg.MAP_TILES[transfer_map_tile].get_height()
        map_pos -= cfg.SCROLL_SPEED
        transfer_map_pos -= cfg.SCROLL_SPEED
        #endregion MapScrolling


        #region Draw
        cfg.screen.fill(cfg.grey)

        cfg.screen.blit(cfg.MAP_TILES[map_tile], (0, screenheight - map_pos))
        cfg.screen.blit(cfg.MAP_TILES[transfer_map_tile], (0, screenheight - transfer_map_pos))

        # pygame.draw.rect(cfg.screen, red, cfg.player.rect, 1)
        cfg.live_sprites.draw(cfg.screen)

        cfg.screen.blit(score_text, ((screenwidth - score_text.get_width()) / 2, 5 * SCREEN_SCALE))
        text = cfg.SMALL_FONT.render(str(cfg.score), True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, score_text.get_height() + 7 * SCREEN_SCALE))

        if game_over:
            game_over += 1
            if game_over > cfg.DEATH_SCREEN_TICKS:
                return 0
            if game_over > cfg.DEATH_SCREEN_TICKS // 8:
                text = cfg.LARGE_FONT.render("GAME OVER", True, cfg.red)
                cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2))
            elif game_over == cfg.DEATH_SCREEN_TICKS // 8:
                cfg.GAME_OVER_MUSIC.play()


        pygame.display.flip()
        #endregion Draw

        cfg.clock.tick(60)
    return -1

def cleanup() -> None:
    seed("1942")
    for sprite in cfg.live_sprites.sprites():
        sprite.kill()
    cfg.screen.fill(cfg.black)
    pygame.display.flip()
    cfg.score = 0

def main_menu() -> bool:
    pygame.display.set_caption("1942")
    running = True
    ticks = 0
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return True

        cfg.screen.fill(cfg.black)
        cfg.screen.blit(cfg.LOGO, ((screenwidth - cfg.LOGO.get_width()) / 2, screenheight / 2 - cfg.LOGO.get_height()))
        text = cfg.SMALL_FONT.render("Press Enter to Start", True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2 + 2 * text.get_height()))
        pygame.display.flip()
        cfg.clock.tick(60)

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
