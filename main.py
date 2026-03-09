from core.game import Game
from core.window import Window
from core.context import ContextDisplay

def main():
    window: Window = Window()
    ContextDisplay.screen, ContextDisplay.surface = window.screen, window.surface

    game = Game()
    game.run()

if __name__ == '__main__':
    main()
