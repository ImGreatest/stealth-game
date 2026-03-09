import pygame

from core.const import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_PADDING


class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface = self.screen.subsurface(SCREEN_PADDING, SCREEN_PADDING, SCREEN_WIDTH - 2 * SCREEN_PADDING, SCREEN_HEIGHT - 2 * SCREEN_PADDING)
        pygame.display.set_caption("Game")
        pygame.mouse.set_visible(True)
