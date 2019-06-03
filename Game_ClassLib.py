
import random
import pygame
import Main_Game as Main


# global variables
player_img = pygame.image.load("Img/playerShip1_orange.png")
bullet_img = pygame.image.load("Img/laserBlue16.png")
evilbullet_image = pygame.image.load("Img/laserRed16.png")
enemy_moving_list = [-3, -2, -1, 0, 1, 2, 3]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 48))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, (0, 255, 0), self.rect.center, self.radius)
        self.rect.centerx = Main.screen_width/2
        self.rect.bottom = Main.screen_height
        self.speedx = 0
        self.speedy = 0
        self.LIFE = 100
        self.shoot_sound = pygame.mixer.Sound("Game_Sound/player_shoot.wav")
        self.hitted_sound = pygame.mixer.Sound("Game_Sound/player_hitted.wav")

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        # keyboard movements
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # screen delimiter
        if self.rect.right > Main.screen_width:
            self.rect.right = Main.screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Main.screen_height:
            self.rect.bottom = Main.screen_height

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        self.shoot_sound.play()


class Enemy(pygame.sprite.Sprite):

    # list ogìf images fon enemies ship
    list_images = []
    for i in range(1, 5):
        filename = "enemyBlack{}.png".format(i)
        img = pygame.image.load("Img/Enemies/" + filename)
        img.set_colorkey((0, 0, 0))
        img_scaled = pygame.transform.scale(img, (50, 50))
        list_images.append(img_scaled)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # temp
        self.image = random.choice(self.list_images)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, (0, 255, 0), self.rect.center, self.radius)
        self.rect.x = random.randrange(Main.screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -60)
        self.speedy = 0
        self.speedx = 0
        self.moving = 0
        self.entered = False
        self.shoot_sound = pygame.mixer.Sound("Game_Sound/enemy_shoot.wav")
        self.explode_sound = pygame.mixer.Sound("Game_Sound/enemy_explode.wav")

    def update(self):
        # if is not on the screen, the sprite go simply ahead
        if self.entered:
            if self.moving == 0:
                self.randmove()
            else:
                self.moving -= 1
        else:
            self.speedy = 1
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # enemy is on screen
        if self.rect.y > 0:
            self.entered = True
        # screen delimiter
        if self.rect.right > Main.screen_width:
            self.rect.right = Main.screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0 and self.entered:
            self.rect.top = 0
        if self.rect.bottom > Main.screen_height/2:
            self.rect.bottom = Main.screen_height/2

    def randmove(self):
        self.moving = 80
        self.speedx = random.choice(enemy_moving_list)
        self.speedy = random.choice(enemy_moving_list)

    def shoot(self, all_sprites, evil_bullets):
        evilbullet = EvilBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(evilbullet)
        evil_bullets.add(evilbullet)
        self.shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (8, 20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if goes out-screen
        if self.rect.bottom < 0:
            self.kill()


class EvilBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(pygame.transform.scale(evilbullet_image, (8, 20)), False, True)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 6

    def update(self):
        self.rect.y += self.speedy
        # kill if it goes out of screen
        if self.rect.top > Main.screen_height:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, explosion_anim):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.explosion_anim = explosion_anim

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Backgrounds(pygame.sprite.Sprite):

    list_backs = []
    list_prob = [0.3, 0.5, 0.2]

    # load background images
    img_meteor_brown_lg = pygame.transform.scale(pygame.image.load("Img/Background/Mobs/meteorBrown_big3.png"),
                                                 (50, 50))
    list_backs.append(img_meteor_brown_lg)
    img_meteor_brown_md = pygame.transform.scale(pygame.image.load("Img/Background/Mobs/meteorBrown_med1.png"),
                                                 (25, 25))
    list_backs.append(img_meteor_brown_md)
    img_meteor_brown_sm = pygame.transform.scale(pygame.image.load("Img/Background/Mobs/meteorBrown_tiny1.png"),
                                                 (10, 10))
    list_backs.append(img_meteor_brown_sm)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choices(self.list_backs, self.list_prob, k=1)[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(Main.screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedx = 0
        self.speedy = random.randrange(3, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it goes out of screen
        if self.rect.top > Main.screen_height:
            self.kill()


