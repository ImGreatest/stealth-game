from __future__ import annotations

import pygame

from base import Updatable, Drawable
from const import MISSING_TEXTURE
from context import Display
from interfaces import SpriteData


class Sprite(Updatable, Drawable):
    def __init__(
            self,
            position: tuple,
            # sprite_data: SpriteData | None,
            sprite_name: str | None,
            size: tuple = (16, 16),
            visible: bool = True,
    ):
        self._sprite_position = position
        self._sprite_size = size
        self._sprite_visible = visible
        self._sprite_name = self._define_sprite_name(sprite_name)

        self.original_surface = pygame.image.load(self.get_sprite_pathway()).convert_alpha()
        self.original_surface = pygame.transform.scale(self.original_surface, self._sprite_size)

        self.sprite_surface = self.original_surface.copy()
        self.sprite_rect = self.sprite_surface.get_rect(center=self._sprite_position)

    @property
    def sprite_position(self):
        return self._sprite_position

    @sprite_position.setter
    def sprite_position(self, new_sprite_position: tuple):
        self._sprite_position = new_sprite_position

    @property
    def sprite_size(self):
        return self._sprite_size

    @sprite_size.setter
    def sprite_size(self, new_sprite_size: tuple):
        self._sprite_size = new_sprite_size

    @property
    def sprite_visible(self):
        return self._sprite_visible

    @sprite_visible.setter
    def sprite_visible(self, new_sprite_visible: bool):
        self._sprite_visible = new_sprite_visible

    @staticmethod
    def _define_sprite_data(sprite_data: SpriteData | None) -> SpriteData:
        if sprite_data is None:
            return MISSING_TEXTURE
        return sprite_data

    @staticmethod
    def _define_sprite_name(name: str | None):
        if name is None:
            return "missing-texture"
        return name

    def get_sprite_pathway(self):
        return "assets/" + self._sprite_name + ".png"

    def draw(self, **kwargs: object) -> None:
        """
        Drawing the sprite on the screen

        :rtype: None
        """
        if self._sprite_visible:
            Display.screen.blit(self.sprite_surface, self.sprite_rect)
        super().draw(Display.screen)

    def update(self, parent_x: int, parent_y: int, angle: float):
        self.sprite_surface = pygame.transform.rotate(self.original_surface, angle)

        self.sprite_rect = self.sprite_surface.get_rect(center=(parent_x, parent_y))
        self._sprite_position = self.sprite_rect.center
        super().update(parent_x, parent_y, angle)


class Hitbox(Updatable, Drawable):
    def __init__(
            self,
            position: tuple,
            size: tuple,
            offset_x: int = 0,
            offset_y: int = 0,
            visible: bool = False,
    ):
        self._hitbox_position = position
        self._hitbox_size = size
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._visible = visible

        self.hitbox_surface = pygame.Surface(self._hitbox_size, pygame.SRCALPHA)
        self.hitbox_surface.fill((255, 255, 255))

        self.hitbox_rect = self.hitbox_surface.get_rect(center=self._hitbox_position)
        self.mask = pygame.mask.from_surface(self.hitbox_surface)

    @property
    def hitbox_position(self) -> tuple:
        return self._hitbox_position

    @hitbox_position.setter
    def hitbox_position(self, new_positon: tuple):
        self._hitbox_position = new_positon

    @property
    def hitbox_size(self) -> tuple:
        return self._hitbox_size

    @hitbox_size.setter
    def hitbox_size(self, new_size: tuple):
        self._hitbox_size = new_size

    @property
    def offset_x(self) -> int:
        return self._offset_x

    @offset_x.setter
    def offset_x(self, new_offset_x: int):
        self._offset_x = new_offset_x

    @property
    def offset_y(self) -> int:
        return self._offset_y

    @offset_y.setter
    def offset_y(self, new_offset_y: int):
        self._offset_y = new_offset_y

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, new_visible: bool):
        self._visible = new_visible

    def update(self, parent_x: int, parent_y: int, angle: float) -> None:
        """ Update the position of the hitbox follow of parent
        :param angle:
        :param parent_x
        :param parent_y
        """
        rotated_hitbox_surf = pygame.transform.rotate(self.hitbox_surface, angle)
        self.mask = pygame.mask.from_surface(rotated_hitbox_surf)
        target_center = (parent_x + self._offset_x, parent_y + self._offset_y)
        self.hitbox_rect = rotated_hitbox_surf.get_rect(center=target_center)

        super().update(parent_x, parent_y, angle)

    def collide_with(self, other_hitbox: Hitbox) -> bool:
        """ Check if the hitbox collides with something
        :param other_hitbox:
        :return:
        :rtype: bool
        :return:
        """
        if self.hitbox_rect.colliderect(other_hitbox.hitbox_rect):
            offset = (other_hitbox.hitbox_rect.x - self.hitbox_rect.x, other_hitbox.hitbox_rect.y - self.hitbox_rect.y)

            overlap_point = self.mask.overlap(other_hitbox.mask, offset)
            return overlap_point is not None

        return False

    def draw(self, color: tuple = (255, 0, 0), **kwargs: object) -> None:
        """ Draw the hitbox on the screen
        :param color
        """
        actual_color = color if isinstance(color, (tuple, list, pygame.Color)) else (255, 0, 0)

        if self._visible:
            # pygame.draw.rect(screen, (100, 100, 100), self.hitbox_rect)

            mask_surface = self.mask.to_surface(setcolor=actual_color, unsetcolor=(0, 0, 0, 0))
            Display.screen.blit(mask_surface, self.hitbox_rect)

        super().draw(Display.screen)

    def update_mask(self, surface: pygame.Surface) -> None:
        self.mask = pygame.mask.from_surface(surface)

    def rotate(self, angle: int):
        self._angle = angle

        rotated_surface = pygame.transform.rotate(self.hitbox_surface, self._angle)
        self.mask = pygame.mask.from_surface(rotated_surface)

        old_center = self.hitbox_rect.center
        self.hitbox_rect = rotated_surface.get_rect(center=old_center)
        self._hitbox_size = self.hitbox_rect.size
