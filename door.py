import pygame

from game_object import GameObject


class Door(GameObject):
    def __init__(self, position: tuple, sprite_size: tuple):
        super().__init__(position, sprite_size)
        self.opened = True
        self.color = pygame.Color("red")

    def update(self, screen: pygame.Surface):
        pass
