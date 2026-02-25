import sys

import pygame

from core.window import Window
from core.context import ContextDisplay
from game import Game

pygame.init()

def main():
    ContextDisplay.screen = Window().screen
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            game.update()

            pygame.display.flip()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
