import pygame

from context import Display
from effects import EffectManager
from player import Player
from wall import Wall


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.effect_manager = EffectManager()
        self.player = Player((100, 300))
        self.wall = Wall(100, 500, (50, 25))

    def tick(self):
        self.clock.tick(self.fps)

    def draw(self):

        Display.screen.fill((20, 20, 40))

        self.effect_manager.draw()
        self.wall.draw()
        self.player.draw()

    def update(self):
        self.player.update()
        self.effect_manager.update()
