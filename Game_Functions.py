
import pygame
import random
import Main_Game as Main
import Game_ClassLib as Lib


font_name = pygame.font.match_font('consolas')


def enemy_shoot(enemies, all_sprites, evil_bullets):
    shooter = random.choice(enemies.sprites())
    shooter.shoot(all_sprites, evil_bullets)


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_life(surface, life, x, y):
    bar_lenght = 100
    bar_height = 10
    fill = (life / 100) * bar_lenght
    outline_rect = pygame.Rect(x, y, bar_lenght, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)


def show_gameover_screen(screen, clock, score):
    screen.blit(Main.background_game_over, Main.background_go_rect)
    draw_text(screen, "A.S.T.W.D.N.", 64, Main.screen_width / 2, Main.screen_height / 4)
    draw_text(screen, "Arrow keys move, A to fire", 22,
              Main.screen_width / 2, Main.screen_height / 2)
    if score != 0:
        draw_text(screen, "Your Score: " + str(score), 22, Main.screen_width / 2, Main.screen_height - 100)
    draw_text(screen, "Press space bar to begin", 18, Main.screen_width / 2, Main.screen_height - 30)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(Main.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False


def spawn_backs(all_sprites, backgrounds):
    back = Lib.Backgrounds()
    backgrounds.add(back)




