import pygame

class SpriteSheet:
    def __init__(self, file_path : str, columns : int, rows : int, crop : None|pygame.Rect = None) -> None:
        self.sheet = pygame.image.load(file_path).convert_alpha()
        if crop is not None:
            self.sheet = self.sheet.subsurface(crop)
        self._columns = columns
        self._rows = rows
        self.rect = self.sheet.get_rect()
        self._cell_width = self.rect.width / columns
        self._cell_height = self.rect.height / rows

    def image_at(self, column : int, row : int) -> pygame.Surface:
        return self.sheet.subsurface((self._cell_width * column, self._cell_height * row, self._cell_width, self._cell_height))

    def load_strip(self, row, count : int) -> list[pygame.Surface]:
        return [self.image_at(i, row) for i in range(count)]