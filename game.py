import pygame
import sys
import os
import random


FPS = 60
size = WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Бегущий динозавр')
game_over = False
pause = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Dino(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.frames = [pygame.transform.scale(load_image('динозавр1.png'), (200, 200)),
                       pygame.transform.scale(load_image('динозавр2.png'), (200, 200)),
                       pygame.transform.scale(load_image('динозавр3.png'), (200, 200)),
                       pygame.transform.scale(load_image('динозавр4.png'), (200, 200))]
        self.cur_frame = 12
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isJump = False
        self.jumpSpeed = 11
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not game_over and not pause:
            if self.cur_frame == 12:
                self.cur_frame = 0
            self.image = self.frames[self.cur_frame // 4]
            self.cur_frame += 1
            if self.isJump:
                if self.jumpSpeed >= -11:
                    if self.jumpSpeed < 0:
                        self.rect.y += (self.jumpSpeed ** 2) // 1.8
                    else:
                        self.rect.y -= (self.jumpSpeed ** 2) // 1.8
                    self.jumpSpeed -= 1
                    self.image = self.frames[0]
                else:
                    self.jumpSpeed = 11
                    self.isJump = False


class Cactus(pygame.sprite.Sprite):
    image = load_image('кактус.png')

    def __init__(self, group, size, x, y):
        super().__init__(group)
        self.group = group
        self.image = Cactus.image
        self.image = pygame.transform.scale(self.image, (size - 30, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not game_over and not pause:
            self.rect.x -= 13
            if self.rect.x + self.image.get_width() < 0:
                self.group.remove(self)


def gameover(group1, group2):
    global game_over
    for i in group1:
        for j in group2:
            if pygame.sprite.collide_mask(i, j):
                game_over = True
                font = pygame.font.Font('data/font.otf', 70)
                text = font.render('Game over', True, (0, 100, 0))
                text_x = WIDTH // 2 - text.get_width() // 2
                text_y = 100
                screen.blit(text, (text_x, text_y))
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
                    pygame.display.flip()
                    clock.tick(FPS)


def pause_game():
    global pause
    if pause is False:
        pause = True
    else:
        pause = False


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((135, 206, 250))
    sand = load_image('fon.png')
    sand = pygame.transform.scale(sand, (800, 150))
    screen.blit(sand, (0, HEIGHT - sand.get_height()))
    font = pygame.font.Font('data/font.otf', 70)
    text = font.render('Бегущий динозавр', True, (0, 100, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = 100
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font('data/font.otf', 35)
    text = font.render('Правила игры:', True, (0, 100, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = 300
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font('data/font.otf', 35)
    text = font.render('Нажимайте пробел чтобы прыгать', True, (0, 100, 0))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = 350
    screen.blit(text, (text_x, text_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def game():
    screen.fill((135, 206, 250))
    sand = load_image('fon.png')
    sand = pygame.transform.scale(sand, (800, 150))
    screen.blit(sand, (0, HEIGHT - sand.get_height()))
    cactus_sprites = pygame.sprite.Group()
    dino_sprites = pygame.sprite.Group()
    dino = Dino(dino_sprites, 100, 300)
    size_cactus = random.randrange(100, 151, 50)
    a = WIDTH
    Cactus(cactus_sprites, size_cactus, a, HEIGHT - sand.get_height() - size_cactus + 50)
    a += 500
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dino.isJump = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game()
        gameover(dino_sprites, cactus_sprites)
        size_cactus = random.randrange(100, 151, 50)
        a += 500
        Cactus(cactus_sprites, size_cactus, a, HEIGHT - sand.get_height() - size_cactus + 50)
        screen.fill((135, 206, 250))
        screen.blit(sand, (0, HEIGHT - sand.get_height()))
        cactus_sprites.draw(screen)
        cactus_sprites.update()
        dino_sprites.draw(screen)
        dino_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    start_screen()
    game()
