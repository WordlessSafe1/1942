import pygame
import config as cfg

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x:int|float, y:int|float, type:int = 0):
        """
        Initialize an Explosion
        @param type - 0: Enemy, 1: Player
        """
        pygame.sprite.Sprite.__init__(self)
        if type == 0:
            cfg.FIZZLE_SOUND.play()
            self._images = cfg.EXPLOSION_IMAGES
        else:
            cfg.BGM.stop()
            cfg.EXPLOSION_SOUND.play()
            self._images = cfg.PLAYER_EXPLOSION_IMAGES
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