import pygame
import sys
import os
import pyganim
import random


FPS = 60
size = WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Бегущий динозавр')


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


class Dino:
    def __init__(self, x, y):
        run_sprites = []
        run_sprites.append(pygame.transform.scale(load_image('динозавр1.png'), (200, 200)))
        run_sprites.append(pygame.transform.scale(load_image('динозавр2.png'), (200, 200)))
        run_sprites.append(pygame.transform.scale(load_image('динозавр3.png'), (200, 200)))
        run_sprites.append(pygame.transform.scale(load_image('динозавр4.png'), (200, 200)))
        self.runAnim = pyganim.PygAnimation([(run_sprites[0], 70),
                                             (run_sprites[1], 70),
                                             (run_sprites[2], 70),
                                             (run_sprites[3], 70)])
        self.jumpAnim = pyganim.PygAnimation([(run_sprites[0], 70)])
        self.runAnim.play()
        self.jumpAnim.play()
        self.x = x
        self.y = y
        self.isJump = False
        self.jumpSpeed = 11

    def update(self):
        if self.isJump:
            if self.jumpSpeed >= -11:
                if self.jumpSpeed < 0:
                    self.y += (self.jumpSpeed ** 2) / 1.8
                else:
                    self.y -= (self.jumpSpeed ** 2) / 1.8
                self.jumpSpeed -= 1
                self.jumpAnim.blit(screen, (self.x, self.y))
            else:
                self.jumpSpeed = 11
                self.isJump = False
        else:
            self.runAnim.blit(screen, (self.x, self.y))


class Cactus(pygame.sprite.Sprite):
    image = load_image('кактус.png')

    def __init__(self, group, size, x, y):
        super().__init__(group)
        self.image = Cactus.image
        self.image = pygame.transform.scale(self.image, (size - 30, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 13
        if self.rect.x + self.image.get_width() < 0:
            Cactus.kill(self)


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
    dino = Dino(100, 300)
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
        size_cactus = random.randrange(100, 151, 50)
        a += 500
        Cactus(cactus_sprites, size_cactus, a, HEIGHT - sand.get_height() - size_cactus + 50)
        screen.fill((135, 206, 250))
        screen.blit(sand, (0, HEIGHT - sand.get_height()))
        cactus_sprites.draw(screen)
        cactus_sprites.update()
        dino.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    start_screen()
    game()
