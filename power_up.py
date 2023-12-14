from typing import Any
import pygame
import config as cfg

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type:int, x:int, y:int):
        super().__init__()
        self._type = type
        self.image = cfg.POW_IMAGES[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._ttl = cfg.POW_TTL

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.y += cfg.SCROLL_SPEED
        self._ttl -= 1
        if not self._ttl:
            self.kill()
        
        if pygame.sprite.spritecollide(self, cfg.friendly_sprites, False):
            self.kill()
            cfg.live_sprites.add(PointsMark(self.rect.x, self.rect.y))
            match(self._type):
                case cfg.POW_RED:    cfg.score += 1000                            # 1000 pts
                case cfg.POW_BLACK:  cfg.lives += 1;            cfg.score += 1000 # Xtra Life
                case cfg.POW_YELLOW: pass                                         # Xtra Stage Loops
                case cfg.POW_GREY:   pass                                         # Side Fighters
                case cfg.POW_GREEN:  cfg.player.fire_power = 1; cfg.score += 1000 # Main Weapon Upgrade
                case cfg.POW_WHITE:  pass                                         # Kill All Enemies
                case cfg.POW_ORANGE: pass                                         # Stop Enemy Shooting

class PointsMark(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int) -> None:
        super().__init__()
        self.image = cfg.POINT_IMAGE_1000
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._TTL = 60

    def update(self, _keys):
        self.rect.y += cfg.SCROLL_SPEED
        self._TTL -= 1
        if self._TTL <= 0:
            self.kill()
