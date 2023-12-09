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
            match(self._type):
                case cfg.POW_RED:    cfg.score += 1000  # 1000 pts
                case cfg.POW_BLACK:  cfg.lives += 1     # Xtra Life
                case cfg.POW_YELLOW: pass # Xtra Stage Loops
                case cfg.POW_GREY:   pass # Side Fighters
                case cfg.POW_GREEN:  cfg.player.fire_power = 1 # Main Weapon Upgrade
                case cfg.POW_WHITE:  pass # Kill All Enemies
                case cfg.POW_ORANGE: pass # Stop Enemy Shooting
