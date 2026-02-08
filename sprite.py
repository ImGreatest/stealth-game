from dataclasses import dataclass

import pygame

from aseprite_loader import AsepriteLoader
from texture_data import MISSING_TEXTURE


@dataclass
class SpriteData:
    name: str
    frame_key: str
    json_path: str
    png_path: str


class Sprite(pygame.sprite.Sprite):
    def __init__(
            self,
            position: tuple = (0, 0),
            sprite_data: SpriteData = None,
            size: tuple = (16, 16),
            visible: bool = True,
    ):
        super().__init__()
        self._sprite_position = position
        self._sprite_size = size
        self._sprite_visible = visible

        if sprite_data is None:
            self._sprite_data = SpriteData(*MISSING_TEXTURE)
        else:
            self._sprite_data = sprite_data

        self.sprite_frame_key = self._sprite_data.frame_key
        self.sprite_json_path = self._sprite_data.json_path
        self.sprite_png_path = self._sprite_data.png_path

        self.image = pygame.Surface(self._sprite_size)
        self.sprite_rect = self.image.get_rect(topleft=self._sprite_position)

        self.sprite_sheet = AsepriteLoader(self._sprite_data.name)

    @property
    def sprite_position(self) -> tuple:
        return self._sprite_position

    @sprite_position.setter
    def sprite_position(self, value: tuple):
        self._sprite_position = value

    @property
    def sprite_size(self) -> tuple:
        return self._sprite_size

    @sprite_size.setter
    def sprite_size(self, value: tuple):
        self._sprite_size = value

    @property
    def sprite_data(self) -> SpriteData:
        return self._sprite_data

    @sprite_data.setter
    def sprite_data(self, value: SpriteData):
        self._sprite_data = value

    @property
    def sprite_visible(self) -> bool:
        return self._sprite_visible

    @sprite_visible.setter
    def sprite_visible(self, value: bool):
        self._sprite_visible = value

    def draw_sprite(self, screen: pygame.Surface):
        if self._sprite_visible:
            self.sprite_sheet.draw(screen, self.sprite_frame_key, self.sprite_rect.topleft)
