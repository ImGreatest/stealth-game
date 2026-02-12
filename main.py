import sys
import pygame

from context import Display
from event_bus import EventBus
from game import Game
from window import Window

pygame.init()

def main():
    Display.screen = Window().screen
    game = Game()

    running = True
    while running:
        EventBus.process_events()

        game.update()

        game.draw()

        pygame.display.flip()
        game.tick()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
