import sys
import pygame

from game import Game
from window import Window

pygame.init()

def main():
    window = Window()
    game = Game()

    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        game.update(events)

        game.draw(window.screen)

        pygame.display.flip()
        game.tick()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
