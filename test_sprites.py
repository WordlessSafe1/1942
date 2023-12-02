import pygame
from pygame.locals import *

SCREEN_SCALE = 2


screenheight = 400 * SCREEN_SCALE
screenwidth  = 200 * SCREEN_SCALE

pygame.init()
screen = pygame.display.set_mode([screenwidth, screenheight], pygame.SCALED, vsync=1)
clock = pygame.time.Clock()

orig_sheet = pygame.image.load("resources/img/Sprites.png").convert()
offset_x = 1
offset_y = 0
size_x = 255
size_y = 50
#bullet: 74,89,6,6
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT] and offset_x + size_x < orig_sheet.get_width():
        offset_x += 1
    if keys[K_LEFT] and offset_x > 0:
        offset_x -= 1
    if keys[K_UP] and offset_y > 0:
        offset_y -= 1
    if keys[K_DOWN] and offset_y + size_y < orig_sheet.get_height():
        offset_y += 1
    if keys[K_w] and size_y > 0:
        size_y -= 1
    if keys[K_s] and offset_y + size_y < orig_sheet.get_height():
        size_y += 1
    if keys[K_a] and size_x > 0:
        size_x -= 1
    if keys[K_d] and offset_x + size_x < orig_sheet.get_width():
        size_x += 1

    
    sprite = orig_sheet.subsurface(pygame.Rect(offset_x, offset_y, size_x, size_y))


    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(sprite, (sprite.get_width() * SCREEN_SCALE, sprite.get_height() * SCREEN_SCALE)).convert(), (0, 0))
    font = pygame.font.SysFont("monospace", 15)
    # print offset_x, offset_y, size_x, size_y
    label = font.render(f"o_x: {offset_x}, o_y: {offset_y}, s_x: {size_x}, s_y: {size_y}", 1, (255,255,0))
    screen.blit(label, (0, screenheight - 15))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, size_x * SCREEN_SCALE, size_y * SCREEN_SCALE), 1)

    pygame.display.flip()

    clock.tick(60)
    pass