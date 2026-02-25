import pygame


class Window:
    def __init__(self):
        self.screen = pygame.display.set_mode((1600, 800))
        pygame.display.set_caption("Game")
        pygame.mouse.set_visible(True)
