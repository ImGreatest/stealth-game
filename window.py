import pygame

from const import SCREEN_WIDTH, SCREEN_HEIGHT


class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game")
        pygame.mouse.set_visible(True)
