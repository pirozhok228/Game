import pygame
import sys


FPS = 60
size = WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game')


def terminate():
    pygame.quit()
    sys.exit()


def game():
    screen.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    game()
