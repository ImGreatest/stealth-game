import pygame

from core.context import ContextDisplay
from entities.player import Player
from tools.enviroments import FogOfWar
from tools.ui import UIScreen

clock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.dt = 0.0
        self.fps = 60

        self.player = Player((100, 100))
        # self.fog = FogOfWar(800, 600)
        self.ui_screen = UIScreen(self.player)

    def tick(self):
        self.dt = clock.tick(self.fps) /  1000.0

        return self.dt

    def update(self):
        dt = self.tick()

        ContextDisplay.screen.fill((20, 20, 40))

        self.player.update(dt)
        # self.fog.update([self.player.player_vision])

        self.player.draw()
        # self.fog.draw()

        self.ui_screen.blit(f"FPS {int(clock.get_fps())}")
