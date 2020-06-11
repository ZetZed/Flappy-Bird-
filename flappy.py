import pygame
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    pygame.display.update()