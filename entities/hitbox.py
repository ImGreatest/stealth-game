import pygame

from core.base import Updatable, Drawable
from core.context import ContextDisplay


class Hitbox(Updatable, Drawable):
    def __init__(self, position: tuple, size: tuple = (16, 16), offset: tuple = (0, 0)):
        self._hitbox_position = pygame.math.Vector2(position)
        self._hitbox_size = size
        self.offset = pygame.math.Vector2(offset)

        self.last_angle = None

        self.hitbox_surface = pygame.Surface(self._hitbox_size, pygame.SRCALPHA)
        self.hitbox_surface.fill((122, 122, 122))
        self.hitbox_rect = self.hitbox_surface.get_rect(center=self._hitbox_position)
        self.mask = pygame.mask.from_surface(self.hitbox_surface)
        self.mask_surface: pygame.Surface | None = None

    @property
    def hitbox_position(self):
        pass

    @hitbox_position.setter
    def hitbox_position(self, value: pygame.math.Vector2):
        self._hitbox_position = value

    @hitbox_position.getter
    def hitbox_position(self) -> pygame.math.Vector2:
        return self._hitbox_position

    @property
    def hitbox_size(self):
        pass

    @hitbox_size.setter
    def hitbox_size(self, value: tuple):
        self._hitbox_size = value

    @hitbox_size.getter
    def hitbox_size(self) -> tuple:
        return self._hitbox_size

    def collide_with(self, other_hitbox: "Hitbox") -> bool:
        if self.hitbox_rect.colliderect(other_hitbox.hitbox_rect):
            offset = (other_hitbox.hitbox_rect.x - self.hitbox_rect.x, other_hitbox.hitbox_rect.y - self.hitbox_rect.y)

            overlap_point = self.mask.overlap(other_hitbox.mask, offset)
            return overlap_point is not None

        return False

    def draw(self, color: tuple = None, **kwargs) -> None:
        if color is not None:
            self.mask_surface = self.mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))

        if self.mask_surface is None:
            default_color = (255, 255, 255)
            self.mask_surface = self.mask.to_surface(setcolor=default_color, unsetcolor=(0, 0, 0, 0))

        if self.mask_surface:
            ContextDisplay.screen.blit(self.mask_surface, self.hitbox_rect)

        self.mask_surface = None

        super().draw()

    def update(self, dt: float, parent_x: float, parent_y: float, angle: float):
        rotated_hitbox_surf = pygame.transform.rotate(self.hitbox_surface, angle)
        self.mask = pygame.mask.from_surface(rotated_hitbox_surf)
        target_center = (parent_x + self.offset.x, parent_y + self.offset.y)
        self.hitbox_rect = rotated_hitbox_surf.get_rect(center=target_center)

        super().update(dt, parent_x, parent_y, angle)