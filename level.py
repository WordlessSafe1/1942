import pygame
from config import screenwidth, screenheight, ENEMY_SIZE
from character import Enemy

GAME_MAP: list[int] = None
ENEMY_PATHS: dict[str, list[tuple[int|float,int|float,int,int,int]]] = None
ENEMY_WAVES: list[tuple[int, Enemy, tuple[int|float, int|float, int, int, int]]] = None

def init():
    global GAME_MAP, ENEMY_PATHS, ENEMY_WAVES
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

        (200, Enemy, (2.5 * ENEMY_SIZE[0],             -ENEMY_SIZE[1], ENEMY_PATHS["cross left wide"],        0, -50, 42)),
        ( 50, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
        ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0,  15)),
        ( 90, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0, 110)),
        ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0,  73)),
        ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0,  150)),
        ( 30, Enemy, (screenwidth,                   screenheight / 2, ENEMY_PATHS["loop left"],              0,  0)),
        (  0, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
        ( 20, Enemy, (2 * ENEMY_SIZE[0],               -ENEMY_SIZE[1], ENEMY_PATHS["cross right wide"],            0,  25)),
        ( 25, Enemy, (screenwidth - 3 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,   0,  15)),

        (250, Enemy, (screenwidth - 2 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
        ( 20, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
        ( 25, Enemy, (screenwidth - 3.5*ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,   0)),
        ( 20, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right wide"],       0, -25, 160)),
        (  0, Enemy, (screenwidth - 2 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross left wide"],        0, -50, 160)),
        ( 50, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
        ( 30, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
        ( 20, Enemy, (screenwidth - 4 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
        ( 25, Enemy, (screenwidth - 3 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,   0)),

        (200, Enemy, (screenwidth - 2 * ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross left"],             0,  25, 160)),
        ( 20, Enemy, (screenwidth - ENEMY_SIZE[0],     -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,  25)),
        ( 25, Enemy, (screenwidth - 3.5*ENEMY_SIZE[0], -ENEMY_SIZE[1], ENEMY_PATHS["cross right"],            0,   0)),
        ( 20, Enemy, (ENEMY_SIZE[0],                   -ENEMY_SIZE[1], ENEMY_PATHS["cross right wide"],       0, -25, 160)),
        ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],             0,  0, 400)),
        ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],             0,  0)),
        ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],             0,  0,  95)),
        ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],             0,  0)),
        ( 30, Enemy, (-ENEMY_SIZE[0],                screenheight / 4, ENEMY_PATHS["loop right"],             0,  0)),

        
        (250, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],              0,  0, 80)),
        (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 3, ENEMY_PATHS["loop right"],             0,  0, 17)),
        ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],              0,  0)),
        (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 3, ENEMY_PATHS["loop right"],             0,  0, 41)),
        ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],              0,  0)),
        (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 3, ENEMY_PATHS["loop right"],             0,  0, 33)),
        ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],              0,  0, 160)),
        (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 3, ENEMY_PATHS["loop right"],             0,  0)),
        ( 30, Enemy, (screenwidth,                   screenheight / 4, ENEMY_PATHS["loop left"],              0,  0, 95)),
        (  0, Enemy, (-ENEMY_SIZE[0],                screenheight / 3, ENEMY_PATHS["loop right"],             0,  0)),




        (None, None, -1), # Wait infinitely until the game ends
    ]
    return
