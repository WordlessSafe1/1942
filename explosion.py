import pygame
import config as cfg
from power_up import PowerUp
from random import choices, randint

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x:int|float, y:int|float, type:int):
        """
        Initialize an Explosion
        @param type - 0: Player, 1: Enemy, 2: Boss
        """
        pygame.sprite.Sprite.__init__(self)
        match(type):
            case 0:
                if cfg.bgm_timer != None:
                    cfg.bgm_timer.cancel()
                    cfg.bgm_timer = None
                pygame.mixer.stop()
                cfg.EXPLOSION_SOUND.play()
                self._images = cfg.PLAYER_EXPLOSION_IMAGES
            case 1:
                cfg.FIZZLE_SOUND.play()
                self._images = cfg.EXPLOSION_IMAGES
            case 2:
                cfg.EXPLOSION_SOUND.play()
                self._images = cfg.BIG_EXPLOSION_IMAGES
        self.image = self._images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._frame = 0
        self._ticks = 0
        self._type = type

    def update(self, _keys):
        self._ticks += 1
        if not self._ticks % 5:
            self._frame += 1
            if self._frame >= len(self._images):
                self.kill()
                POWS = [cfg.POW_RED, cfg.POW_GREEN, cfg.POW_BLACK]
                if self._type and randint(0, 20 // (self._type ** 3)):
                    return
                match(self._type):
                    case 1: pow_type = choices(POWS, [100, 50, 20])[0]
                    case 2: pow_type = choices(POWS, [  1, 30, 50])[0]
                    case _: return
                pow = PowerUp(pow_type, self.rect.x, self.rect.y)
                cfg.live_sprites.add(pow)
                return
            self.image = self._images[self._frame]