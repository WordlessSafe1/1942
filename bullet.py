import pygame
import config


class Bullet(pygame.sprite.Sprite):
    _SPEED = 5 * config.SCREEN_SCALE
    def __init__(self, x, y, style, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        if style not in config.bullet_sprites.keys():
            raise ValueError(f"Invalid bullet style: {style}")
        self.image = config.bullet_sprites[style]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._style = style
        self._dx = dx
        self._dy = dy

    def update(self, _keys):
        self.rect.y -= self._SPEED * self._dy
        self.rect.x += self._SPEED * self._dx
        if self.rect.y < -self.rect.height:
            self.kill()
            return
        targets = config.friendly_sprites if self._style == "enemy" else config.hostile_sprites
        for target in targets:
            if pygame.sprite.collide_mask(self, target):
                target.hit()
                if self._style == "power":
                    target.hit()
                self.kill()
                return