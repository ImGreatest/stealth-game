import math
from enum import Enum
from typing import Optional

import pygame

from base import GameObject
from entities import Hitbox, Sprite


class PlayerDirectionView(Enum):
    IDLE = 'idle'
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    UP_LEFT = 'up_left'
    UP_RIGHT = 'up_right'
    DOWN_LEFT = 'down_left'
    DOWN_RIGHT = 'down_right'


class Player(GameObject, Sprite, Hitbox):
    def __init__(self, position: tuple, size: tuple = (16, 16),):
        GameObject.__init__(self)
        Sprite.__init__(self, position, None)
        Hitbox.__init__(self, position, size)

        self._position = position
        self._size = size

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.direction_view = None

        self.input_controller = InputController(self)
        self.mouse_controller = MouseController(self)

    @property
    def velocity(self):
        return self.velocity_x, self.velocity_y

    @velocity.setter
    def velocity(self, velocity: tuple[float, float]):
        self.velocity_x, self.velocity_y = velocity

    def update(self, **kwargs: object) -> None:
        """
        Update aspects of the player

        :param kwargs:
        :rtype: None
        """
        self.hitbox_rect.x += self.velocity_x
        self.hitbox_rect.y += self.velocity_y

        self.sprite_rect.x += self.velocity_x
        self.sprite_rect.y += self.velocity_y

        self.input_controller.handle_input()
        self.mouse_controller.handle_input()

        self.update_direction()
        
        super().update(self.hitbox_rect.centerx, self.hitbox_rect.centery, self.mouse_controller.angle)

    def draw(self, **kwargs):
        super().draw()

    def update_direction(self) -> None:
        """
        Update the value of direction player
        :rtype: None
        """
        direction = self.get_direction_from_velocity()

        if not direction is None:
            self.direction_view = direction
        else:
            self.direction_view = PlayerDirectionView.IDLE

    def get_direction_from_velocity(self) -> Optional[PlayerDirectionView]:
        if self.velocity_x == 0 and self.velocity_y == 0:
            return None

        vertical, horizontal = '', ''

        if self.velocity_y < 0: vertical = 'up'
        elif self.velocity_y > 0: vertical = 'down'

        if self.velocity_x > 0: horizontal = 'left'
        elif self.velocity_x < 0: horizontal = 'right'

        if vertical and horizontal:
            name = f"{vertical}_{horizontal}"
        else:
            name = vertical or horizontal

        return PlayerDirectionView(name)


class InputController:
    def __init__(self, player: Player):
        self.player = player

        self.base_speed = 2
        self.sprint_speed = 4

        self.speeds = { False: self.base_speed, True: self.sprint_speed }

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.velocity_x, self.player.velocity_y = 0, 0

        speed = self.speeds[keys[pygame.K_LSHIFT]]

        move_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_a]
        move_y = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_w]

        self.player.velocity_x += move_x * speed
        self.player.velocity_y += move_y * speed


class MouseController:
    def __init__(self, player: Player):
        self.player = player
        self.mouse_pos = (0, 0)
        self.angle = 0

    def handle_input(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self._calculate_rotation()

    def _calculate_rotation(self):
        dx = self.mouse_pos[0] - self.player.hitbox_rect.centerx
        dy = self.mouse_pos[1] - self.player.hitbox_rect.centery

        rads = math.atan2(-dy, dx)
        self.angle = math.degrees(rads)
