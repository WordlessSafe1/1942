import pygame
import os
import config as cfg
from config import SCREEN_SCALE, screenheight, screenwidth
from pygame.locals import *

LEADERBOARD_PATH = "data/leaderboard.txt"

def place_text(place: int) -> str:
    match place:
        case 1: return "1ST"
        case 2: return "2ND"
        case 3: return "3RD"
        case 4: return "4TH"
        case 5: return "5TH"
        case 6: return "6TH"
        case 7: return "7TH"
        case 8: return "8TH"
        case 9: return "9TH"
        case _: return f"{place:<3}"

def new_entry():

    running = True
    char_selected = 0
    name = ""
    # A B C D E F G H I J
    # K L M N O P Q R S T
    # U V W X Y Z . - & ?
    # 0 1 2 3 4 5 6 7 8 9
    # ! % ( ) ♂ ♀ ♥   < →
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.-&?0123456789!%()♂♀♥ <→"
    char_size = cfg.SMALL_FONT.size(chars[0])
    block_width = char_size[0] * 10 + 45 * SCREEN_SCALE # 10 * char_width + 5 * 9 * SCREEN_SCALE
    place = -1
    default_score = ("", 0)
    scores = _load_scores()
    for i in range(len(scores)):
        if scores[i][1] < cfg.score:
            place = i + 1
            break
    if place == -1:
        place = len(scores) + 1
    if place <= 5:
        cfg.TOP_LDRBOARD_SOUND.play(loops=-1)
    else:
        cfg.LDRBOARD_SOUND.play()
    place_txt = place_text(place)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.event.post(event)
                return
            if event.type == KEYDOWN and event.key == cfg.CONTROLS[cfg.control_scheme][0]: # Up
                char_selected -= 10
                char_selected %= 50
            elif event.type == KEYDOWN and event.key == cfg.CONTROLS[cfg.control_scheme][1]: # Left
                char_selected -= 1
                char_selected %= 50
            elif event.type == KEYDOWN and event.key == cfg.CONTROLS[cfg.control_scheme][2]: # Down
                char_selected += 10
                char_selected %= 50
            elif event.type == KEYDOWN and event.key == cfg.CONTROLS[cfg.control_scheme][3]: # Right
                char_selected += 1
                char_selected %= 50
            elif event.type == KEYDOWN and event.key == cfg.CONTROLS[cfg.control_scheme][4]: # Space
                if char_selected == 49:
                    _save_score(name, cfg.score)
                    cfg.TOP_LDRBOARD_SOUND.stop()
                    return
                if char_selected == 48:
                    name = name[:-1]
                    continue
                if len(name) >= 8:
                    continue
                name += chars[char_selected]
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                cfg.TOP_LDRBOARD_SOUND.stop()
                return

        cfg.screen.fill(cfg.black)
        for i in range(len(chars)):
            text = cfg.SMALL_FONT.render(chars[i], True, cfg.white)
            x = (i % 10) * (char_size[0] + 5 * SCREEN_SCALE) + (screenwidth - block_width) // 2
            y = (i // 10) * char_size[1] + (100 * SCREEN_SCALE) + (i//10) * 5 * SCREEN_SCALE + (i // 10) * (char_size[1] // 2)
            cfg.screen.blit(text, (x, y))

        x = (char_selected % 10) * (char_size[0] + 5 * SCREEN_SCALE) + (screenwidth - block_width) // 2 - 1.5 * SCREEN_SCALE
        y = (char_selected // 10) * char_size[1] + (100 * SCREEN_SCALE) + (char_selected//10) * 5 * SCREEN_SCALE + (char_selected // 10) * (char_size[1] // 2) - 1 * SCREEN_SCALE
        cfg.screen.blit(cfg.CURSOR_IMAGE, (x, y))

        if len(scores) > 0:
            text = cfg.SMALL_FONT.render(f"TOP {scores[0][1]:>8} {scores[0][0]:<8}", True, cfg.white)
            cfg.screen.blit(text, ((screenwidth - text.get_width()) // 2, (screenheight - text.get_height()) // 2))

        text = cfg.SMALL_FONT.render(f"{place_txt} {cfg.score:>8} {name:<8}", True, cfg.blue)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) // 2, (screenheight - text.get_height()) // 2 + 2 * text.get_height()))

        if place <= len(scores):
            text = cfg.SMALL_FONT.render(f"{place_text(place + 1)} {scores[place - 1][1]:>8} {scores[place - 1][0]:<8}", True, cfg.white)
        else:
            text = cfg.SMALL_FONT.render(f"{place_text(place + 1)} {default_score[1]:>8} {default_score[0]:<8}", True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) // 2, (screenheight - text.get_height()) // 2 + 4 * text.get_height()))
        if place <= len(scores) - 1:
            text = cfg.SMALL_FONT.render(f"{place_text(place + 2)} {scores[place][1]:>8} {scores[place][0]:<8}", True, cfg.white)
        else:
            text = cfg.SMALL_FONT.render(f"{place_text(place + 2)} {default_score[1]:>8} {default_score[0]:<8}", True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) // 2, (screenheight - text.get_height()) // 2 + 6 * text.get_height()))

        text = cfg.SMALL_FONT.render("Press ESC to skip", True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width())/2, screenheight - text.get_height() - 2 * SCREEN_SCALE))


        pygame.display.flip()
        cfg.clock.tick(60)

def _save_score(name: str, score: int) -> None:
    if not os.path.exists("data"):
        os.mkdir("data")
    with open(LEADERBOARD_PATH, "a", encoding='utf-8') as fptr:
        fptr.write(f"{name};{score}\n")

def _load_scores() -> list[tuple[str, int]]:
    scores = []
    if not os.path.exists(LEADERBOARD_PATH):
        return scores
    with open(LEADERBOARD_PATH, "r", encoding='utf-8') as fptr:
        for line in fptr.readlines():
            name, score = line.split(";")
            scores.append((name, int(score)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def show(time:int = -1) -> bool:
    """Returns True if exited with ENTER, False otherwise"""
    scores = _load_scores()

    #region draw
    cfg.screen.fill(cfg.black)
    cfg.screen.blit(cfg.LOGO, ((screenwidth - cfg.LOGO.get_width()) / 2, screenheight / 3 - cfg.LOGO.get_height()))

    for i in range(min(9, len(scores))):
        text = cfg.SMALL_FONT.render(f"{place_text(i + 1)} {scores[i][1]:>8} {scores[i][0]:<8}", True, cfg.white)
        x = (screenwidth - text.get_width()) // 2
        y = (screenheight - text.get_height()) // 3 + i * (text.get_height() + 5 * SCREEN_SCALE) + 10 * SCREEN_SCALE
        cfg.screen.blit(text, (x, y))

    if time == -1:
        text = cfg.SMALL_FONT.render("PRESS ENTER TO CONTINUE", True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) // 2, screenheight - text.get_height() - 10 * SCREEN_SCALE))

    pygame.display.flip()
    #endregion draw

    while time:
        time -= 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.event.post(event)
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return True
        cfg.clock.tick(60)
