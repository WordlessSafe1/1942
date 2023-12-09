import pygame
import config as cfg

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x:int|float, y:int|float, type:int):
        """
        Initialize an Explosion
        @param type - 0: Player, 1: Enemy, 2: Boss
        """
        pygame.sprite.Sprite.__init__(self)
        match(type):
            case 0:
                cfg.BGM.stop()
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

    def update(self, _keys):
        self._ticks += 1
        if not self._ticks % 5:
            self._frame += 1
            if self._frame >= len(self._images):
                self.kill()
                return
            self.image = self._images[self._frame]