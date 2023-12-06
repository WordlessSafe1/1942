import pygame
import config as cfg
from abc import ABC, abstractmethod
from pygame.locals import *
from config import SCREEN_SCALE, screenwidth, screenheight
from bullet import Bullet
from explosion import Explosion

class Character(pygame.sprite.Sprite, ABC):
    @abstractmethod
    def hit(self):
        """Called when the character is hit by an object"""


class Player(Character):
    _L_SPEED = .3                 # Lean speed
    _H_SPEED = 2   * SCREEN_SCALE # Horizontal speed
    _V_SPEED = 2.5 * SCREEN_SCALE # Vertical speed
    _FIRE_COOLDOWN = 6
    _MAX_SHOTS = 3
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._images = cfg.PLAYER_SPRITESHEET.load_strip(0, 7)
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
        collisions = pygame.sprite.spritecollide(self, cfg.hostile_sprites, False)
        if collisions:
            for collision in collisions:
                collision.hit()
            self.hit()
            return

        delta_lean = 0
        if self._fire_cooldown:
            self._fire_cooldown -= 1
        if keys[cfg.CONTROLS[cfg.control_scheme][3]] and self.rect.x + self.rect.width < screenwidth - 5:
            self.rect.x += self._H_SPEED
            delta_lean += self._L_SPEED
        if keys[cfg.CONTROLS[cfg.control_scheme][1]] and self.rect.x > 0:
            self.rect.x -= self._H_SPEED
            delta_lean -= self._L_SPEED
        if keys[cfg.CONTROLS[cfg.control_scheme][0]] and self.rect.y > 0:
            self.rect.y -= self._V_SPEED
        if keys[cfg.CONTROLS[cfg.control_scheme][2]] and self.rect.y + self.rect.height < screenheight:
            self.rect.y += self._V_SPEED
        if keys[cfg.CONTROLS[cfg.control_scheme][4]] and (not self._fire_cooldown) and len(cfg.friendly_fire) < self._MAX_SHOTS:
            bullet = Bullet(self.rect.x + self.rect.width / 2, self.rect.y - 5 * SCREEN_SCALE, "player", 0, 1)
            bullet.rect.x -= bullet.rect.width / 2
            cfg.live_sprites.add(bullet)
            cfg.friendly_fire.add(bullet)
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

    def hit(self):
        pygame.event.post(pygame.event.Event(cfg.GAME_OVER, {"win": False}))
        explosion = Explosion(self.rect.x, self.rect.y, 1)
        cfg.live_sprites.add(explosion)
        super().kill()


class Enemy(Character):
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
        self.image = cfg.ENEMY_SPRITES[frame_x][frame_y]
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
            self.image = cfg.ENEMY_SPRITES[frame_x][frame_y]
        self.x += self._dx
        self.y += self._dy
        self.rect.x = self.x
        self.rect.y = self.y
        self._motion_ticks += 1
        self._dead = False

        if not self._fire_ticks:
            # Fire a bullet towards the player's current position
            dx = cfg.player.rect.x - self.rect.x
            dy = self.rect.y - cfg.player.rect.y
            mag = (dx ** 2 + dy ** 2) ** .5
            mag = max(mag * 2, 2)
            dx /= mag
            dy /= mag
            bullet = Bullet(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height, "enemy", dx, dy)
            bullet.rect.x -= bullet.rect.width / 2
            cfg.live_sprites.add(bullet)

        self._fire_ticks -= 1

    def hit(self):
        super().kill()
        if not self._dead:
            self._dead = True
            cfg.score += 50
            explosion = Explosion(self.rect.x, self.rect.y)
            cfg.live_sprites.add(explosion)
