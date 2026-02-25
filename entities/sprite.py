import pygame

from core.base import Updatable, Drawable
from core.context import ContextDisplay


class Sprite(Updatable, Drawable):
    def __init__(self, sprite_name: str, position: tuple, size: tuple = (16, 16)):
        self._sprite_position = pygame.math.Vector2(position)
        self._sprite_name = sprite_name
        self._sprite_size = size
        self.last_angle = None

        try:
            self.original_sprite = pygame.image.load('assets/missing-texture.png').convert_alpha()
        except FileNotFoundError:
            self.original_sprite = pygame.image.load('assets/' + 'missing-texture' + '.png').convert()
        print(self.original_sprite)
        self.original_sprite = pygame.transform.scale(self.original_sprite, self._sprite_size)

        self.sprite_surface = self.original_sprite.copy()
        self.sprite_rect = self.sprite_surface.get_rect(center=self._sprite_position)

    def draw(self):
        ContextDisplay.screen.blit(self.sprite_surface, self.sprite_rect)
        super().draw()

    def update(self, dt: float, parent_x: float, parent_y: float, angle: float):
        if self.last_angle != angle:
            self.sprite_surface = pygame.transform.rotate(self.original_sprite, angle)
            self.last_angle = angle
        self._sprite_position.update(parent_x, parent_y)
        self.sprite_rect = self.sprite_surface.get_rect(center=self._sprite_position)


        super().update(dt, parent_x, parent_y, angle)
