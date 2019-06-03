
import pygame
import Game_ClassLib as Lib
import Game_Functions as Func

# global variables
screen_width = 900
screen_height = 600
FPS = 60

background_game_over = pygame.image.load("Img/Background/GObackground.jpeg")
background_go_rect = background_game_over.get_rect()


def main():

    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    SCORE = 0

    # backgrounds
    background_purple = pygame.image.load("Img/Background/background_darkPurple_1200.png").convert()
    background_purple_rect = background_purple.get_rect()

    # explosions
    explosion_anim = {}
    explosion_anim['lg'] = []
    explosion_anim['sm'] = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load("Img/Explosion/" + filename).convert()
        img.set_colorkey((0, 0, 0))
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        explosion_anim['sm'].append(img_sm)

    logo = pygame.image.load("Img/koala_icon.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Game")

    # sprites groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    evil_bullets = pygame.sprite.Group()
    backgrounds = pygame.sprite.Group()

    # add backgrounds
    for i in range(8):
        Func.spawn_backs(all_sprites, backgrounds)
    # add player
    player = Lib.Player()
    all_sprites.add(player)
    # add enemies
    for i in range(5):
        enemy = Lib.Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # counters
    main_counter = 0
    seconds_counter = 0

    game_over = True
    running = True

    # main loop ------------------------------------------------------------------------------------------------
    while running:

        clock.tick(FPS)
        main_counter += 1
        # restart on game over
        if game_over:
            Func.show_gameover_screen(screen, clock, SCORE)
            game_over = False
            # re-init all sprites, stats and groups
            all_sprites = pygame.sprite.Group()
            enemies = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            evil_bullets = pygame.sprite.Group()
            backgrounds = pygame.sprite.Group()
            player = Lib.Player()
            all_sprites.add(player)
            for i in range(8):
                Func.spawn_backs(all_sprites, backgrounds)
            for i in range(5):
                enemy = Lib.Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            SCORE = 0

        # every second
        if main_counter == 60:
            seconds_counter += 1
            # enemies shoots
            Func.enemy_shoot(enemies, all_sprites, evil_bullets)
            main_counter = 0
            # score up
            SCORE += 1
            # asteroids
            for i in range(2):
                Func.spawn_backs(all_sprites, backgrounds)

        # event handling --------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.shoot(all_sprites, bullets)

        # update
        all_sprites.update()
        backgrounds.update()

        # check hits ------------------------------------------------------
        #           player-enemy
        p_e_hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
        if p_e_hits:
            game_over = True
        #           enemy-enemy
        for enemy in enemies:
            e_e_hits = pygame.sprite.spritecollide(enemy, enemies, False)
            if len(e_e_hits) > 1:
                enemy.moving = 0
        #           playerbullets-enemy
        b_e_hits = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_circle)
        for hit in b_e_hits:
            enemy = Lib.Enemy()
            enemy.explode_sound.play()
            SCORE += 100
            expl = Lib.Explosion(hit.rect.center, 'lg', explosion_anim)
            all_sprites.add(expl)
            all_sprites.add(enemy)
            enemies.add(enemy)
        #           player-evilbullets
        eb_p_hits = pygame.sprite.spritecollide(player, evil_bullets, True,  pygame.sprite.collide_circle)
        if eb_p_hits:
            for hit in eb_p_hits:
                player.LIFE -= 25
                player.hitted_sound.play()
                expl = Lib.Explosion(hit.rect.center, 'sm', explosion_anim)
                all_sprites.add(expl)
                # check player life
                if player.LIFE <= 0:
                    game_over = True

        # draw-------------------------------------------------------------
        screen.fill((0, 0, 0))
        screen.blit(background_purple, [0, 0])
        backgrounds.draw(screen)
        all_sprites.draw(screen)
        Func.draw_text(screen, str(SCORE), 22, screen_width/2, 20)
        Func.draw_life(screen, player.LIFE, 5, 5)

        # flip
        pygame.display.flip()


if __name__ == "__main__":
    main()
