import pygame
from pygame.locals import *
import level
import config as cfg
from character import Player, init as character_init
import threading
from random import seed
import leaderboard


pygame.init()
cfg.init()
level.init()
character_init()
seed(1942)

SCREEN_SCALE, ENEMY_SIZE, screenheight, screenwidth = cfg.SCREEN_SCALE, cfg.ENEMY_SIZE, cfg.screenheight, cfg.screenwidth


def start_game() -> int:
    """
    Start the game loop.
    Return 0 to restart the game, -1 to quit
    """
    #region Setup
    cfg.BGM.play(loops=-1)
    running = True
    cfg.player = Player()
    cfg.friendly_sprites.add(cfg.player)
    cfg.live_sprites.add(cfg.player)
    map_tile = level.GAME_MAP[0]
    transfer_map_tile = level.GAME_MAP[1]
    map_pos  = 200
    transfer_map_pos = map_pos + cfg.MAP_TILES[transfer_map_tile].get_height()
    next_map_tile = 2
    wave_ticks = 0
    wave = 0
    paused = False
    game_over = 0
    life_lost = 0
    score_text = cfg.SMALL_FONT.render("Score", True, cfg.red)
    locked_lives = cfg.lives
    stage = 0
    stage_cooldown = 0
    #endregion Setup
    while running:
        #region Events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == cfg.LIFE_LOST:
                stored_wavet  = wave_ticks
                stored_index  = wave
                stored_scroll = map_pos
                stored_tile   = map_tile
                stored_nmap   = next_map_tile
                stored_tmap   = transfer_map_tile
                stored_tmap_pos = transfer_map_pos
                cfg.lives -= 1
                if cfg.lives:
                    life_lost = 1
                else:
                    game_over = 1
            elif event.type == KEYDOWN and (not game_over) and event.key == K_ESCAPE:
                if paused:
                    pygame.mixer.unpause()
                    paused = False
                else:
                    pygame.mixer.pause()
                    paused = True
                    text = cfg.LARGE_FONT.render("PAUSED", True, cfg.red)
                    cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2))
                    pygame.display.flip()
        #endregion Events

        if paused:
            continue

        keys = pygame.key.get_pressed()
        cfg.live_sprites.update(keys)

        #region SpawnEnemies
        while wave_ticks == level.ENEMY_WAVES[stage][wave][0]:
            _, type, args = level.ENEMY_WAVES[stage][wave]
            if type == None:
                wave += 1
                continue
            enemy = type(*args)
            cfg.hostile_sprites.add(enemy)
            cfg.live_sprites.add(enemy)
            wave_ticks = 0
            wave += 1
        wave_ticks += 1
        #endregion SpawnEnemies

        #region MapScrolling
        if map_tile == 0 and wave >= len(level.ENEMY_WAVES[stage]) - 1 and wave_ticks >= cfg.STAGE_TRANSITION_TIME:
            stage_cooldown = cfg.STAGE_TRANSITION_TIME
        if map_pos <= 0:
            if next_map_tile >= len(level.GAME_MAP) or stage >= len(level.ENEMY_WAVES):
                ticks = 0
                if cfg.bgm_timer != None:
                    cfg.bgm_timer.cancel()
                    cfg.bgm_timer = None
                cfg.BGM.stop()
                cfg.WIN_MUSIC.play()
                cfg.screen.fill(cfg.black)
                cfg.screen.blit(cfg.LOGO, ((screenwidth - cfg.LOGO.get_width()) / 2, screenheight / 2 - cfg.LOGO.get_height()))
                win_msg = cfg.LARGE_FONT.render("YOU WIN", True, cfg.white)
                cfg.screen.blit(win_msg, ((screenwidth - win_msg.get_width()) / 2, (screenheight + win_msg.get_height()) / 2))
                text = cfg.SMALL_FONT.render(f"Score: {cfg.score} + 100000", True, cfg.white)
                cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight + text.get_height()) / 2 + win_msg.get_height() + 2 * text.get_height()))
                cfg.score += 100000
                for i in range(cfg.lives - 1):
                    cfg.score += 10000
                    text = cfg.SMALL_FONT.render(f"Bonus: +{10000}", True, cfg.white)
                    x = (screenwidth - text.get_width()) / 2
                    y = 5 * SCREEN_SCALE + (screenheight + text.get_height()) / 2 + win_msg.get_height() + 3 * text.get_height() + SCREEN_SCALE * i * text.get_height()
                    cfg.screen.blit(text, (x, y))

                pygame.display.flip()
                while ticks < 500:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            return -1
                    cfg.clock.tick(60)
                    ticks += 1
                return 0
            
            map_tile, transfer_map_tile = transfer_map_tile, level.GAME_MAP[next_map_tile]
            next_map_tile += 1
            map_pos = transfer_map_pos
            transfer_map_pos = map_pos + cfg.MAP_TILES[transfer_map_tile].get_height()
        map_pos -= cfg.SCROLL_SPEED
        transfer_map_pos -= cfg.SCROLL_SPEED
        #endregion MapScrolling

        #region Draw
        cfg.screen.fill(cfg.grey)

        cfg.screen.blit(cfg.MAP_TILES[map_tile], (0, screenheight - map_pos))
        cfg.screen.blit(cfg.MAP_TILES[transfer_map_tile], (0, screenheight - transfer_map_pos))

        cfg.live_sprites.draw(cfg.screen)

        cfg.screen.blit(score_text, ((screenwidth - score_text.get_width()) / 2, 5 * SCREEN_SCALE))
        text = cfg.SMALL_FONT.render(str(cfg.score), True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, score_text.get_height() + 7 * SCREEN_SCALE))

        for i in range(locked_lives - 1):
            cfg.screen.blit(cfg.ENEMY_SPRITES[0][0], (5 + i * (5 + cfg.ENEMY_SIZE[0]), cfg.screenheight - cfg.ENEMY_SIZE[1] - 5))

        #region death
        if game_over:
            game_over += 1
            if game_over > cfg.DEATH_SCREEN_TICKS:
                return 0
            if game_over > cfg.DEATH_SCREEN_TICKS // 8:
                text = cfg.LARGE_FONT.render("GAME OVER", True, cfg.red)
                cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2))
            elif game_over == cfg.DEATH_SCREEN_TICKS // 8:
                cfg.GAME_OVER_MUSIC.play()
        elif life_lost:
            life_lost += 1
            if life_lost > cfg.DEATH_SCREEN_TICKS / 2:
                cleanup()
                wave       = stored_index
                wave_ticks = stored_wavet
                map_pos    = stored_scroll
                map_tile   = stored_tile
                next_map_tile = stored_nmap
                transfer_map_pos = stored_tmap_pos
                transfer_map_tile = stored_tmap
                cfg.player = Player()
                cfg.friendly_sprites.add(cfg.player)
                cfg.live_sprites.add(cfg.player)
                life_lost  = 0
                (cfg.LAST_LIFE_SOUND if cfg.lives == 1 else cfg.LOST_LIFE_SOUND).play()
                cfg.bgm_timer = threading.Timer(5.5, cfg.BGM.play, kwargs={"loops": -1})
                cfg.bgm_timer.start()
        else:
            locked_lives = cfg.lives
        #endregion death

        if stage_cooldown == 1:
            stage += 1
            wave_ticks = -stage_cooldown
            wave = 0
        if stage_cooldown > 0 and not (game_over or life_lost):
            stage_cooldown -= 1
            text = cfg.MEDIUM_FONT.render(f"Stage {stage + 1} complete", True, cfg.white)
            cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2))

        pygame.display.flip()
        #endregion Draw

        cfg.clock.tick(60)
    return -1

def cleanup() -> None:
    for sprite in cfg.live_sprites.sprites():
        sprite.kill()
    cfg.screen.fill(cfg.black)
    pygame.display.flip()

def main_menu() -> bool:
    pygame.display.set_caption("1942")
    running = True
    ticks = 0
    while running:
        ticks += 1
        if not ticks % 600:
            if leaderboard.show(600):
                return True
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return True
            elif event.type == KEYDOWN and event.key == K_l:
                leaderboard.show()
            elif event.type == KEYDOWN and event.key == K_TAB:
                match(cfg.control_scheme):
                    case "arrows":   cfg.control_scheme = "wasd"
                    case "wasd":     cfg.control_scheme = "vim"
                    case "vim":      cfg.control_scheme = "arrows"

        cfg.screen.fill(cfg.black)
        text = cfg.TINY_FONT.render("Control Scheme: " + cfg.control_scheme, True, cfg.white)
        cfg.screen.blit(text, (5 * SCREEN_SCALE, text.get_height()))
        text = cfg.TINY_FONT.render("(TAB to change)", True, cfg.white)
        cfg.screen.blit(text, (5 * SCREEN_SCALE, 3 * text.get_height()))
        cfg.screen.blit(cfg.LOGO, ((screenwidth - cfg.LOGO.get_width()) / 2, screenheight / 2 - cfg.LOGO.get_height()))
        text = cfg.SMALL_FONT.render("Press Enter to Start", True, cfg.white)
        cfg.screen.blit(text, ((screenwidth - text.get_width()) / 2, (screenheight - text.get_height()) / 2 + 2 * text.get_height()))
        pygame.display.flip()
        cfg.clock.tick(60)

def main() -> None:
    pygame.display.set_caption("1942")
    pygame.display.set_icon(cfg.ENEMY_SPRITES[0][1])

    if not main_menu():
        return
    while not start_game():
        leaderboard.new_entry()
        leaderboard.show(300)
        cleanup()
        seed(1942)
        cfg.score = 0
        cfg.lives = cfg.STARTING_LIVES
        if not main_menu(): 
            break
    pygame.quit()
    return




if __name__ == "__main__":
    main()
