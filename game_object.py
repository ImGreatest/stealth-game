import pygame
from sprite import SpriteData, Sprite


class GameObject(Sprite):
    def __init__(
            self,
            position: tuple = (0, 0),
            sprite_data: SpriteData = None,
            sprite_size: tuple[int, int] = (32, 32),
            visible: bool = True,
            hit_box_position: tuple = None,
            hit_box_size: tuple = None,
            object_color: tuple[int, int, int] = (255, 255, 255),
    ):
        super().__init__(position, sprite_data, sprite_size, visible)
        self._object_color = object_color

        if hit_box_position is None:
            self._hit_box_position = self._sprite_position
        else:
            self._hit_box_position = hit_box_position

        if hit_box_size is None:
            self._hit_box_size = self._sprite_size
        else:
            self._hit_box_size = hit_box_size

        self.rect = self.sprite_rect

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self._object_color, self.rect)
        if self._sprite_visible:
            self.sprite_sheet.draw(screen, self.sprite_frame_key, self.sprite_rect.topleft)

    def update(self, events: pygame.event.Event):
        pass
