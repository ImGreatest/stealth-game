from enum import Enum
from typing import Callable

import pygame
from pygame.key import ScancodeWrapper

from core.base import Updatable, Drawable, Tag
from core.const import PLAYER_ROLL_COOLDOWN, KEY_MAP, PLAYER_WALK_SPEED
from core.context import ContextDisplay
from core.states import IdleState, RollState
from tools.obstacle import Obstacle


class PlayerDirectionView(Enum):
    RIGHT = 0
    UP_RIGHT = 1
    UP = 2
    UP_LEFT = 3
    LEFT = 4
    DOWN_LEFT = 5
    DOWN = 6
    DOWN_RIGHT = 7


class Player(Tag, Obstacle, Updatable, Drawable):
    def __init__(self, position: tuple, size: tuple = (16, 16)):
        self.height = 1.75

        Obstacle.__init__(self, position, size)

        self.color = pygame.Color("white")
        self.image.fill(self.color)

        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_surface = None

        self.mouse_angle = None
        self.roll_cooldown = PLAYER_ROLL_COOLDOWN

        self.keymap = KEY_MAP
        self.current_speed = 0.0
        self.is_invulnerable = False
        self.state = IdleState(self)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if self.roll_cooldown > 0:
            self.roll_cooldown -= dt

        new_state = self.state.handle_input(keys, dt)

        if new_state is not self.state:
            if hasattr(self.state, "__exit__"):
                self.state.__exit__(None, None, None)

            self.state = new_state

            if hasattr(self.state, "__enter__"):
                self.state.__enter__()

        self.state.update(dt)

        direction = pygame.math.Vector2(0, 0)
        if any(keys[k] for k in self.keymap["move_up"]):    direction.y -= 1
        if any(keys[k] for k in self.keymap["move_down"]):  direction.y += 1
        if any(keys[k] for k in self.keymap["move_left"]):  direction.x -= 1
        if any(keys[k] for k in self.keymap["move_right"]): direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()

        if not isinstance(self.state, RollState):
            self.velocity = direction * self.current_speed

            # Движение с учетом Delta Time
        self.position += self.velocity * dt

        # Обновление позиции хитбокса
        self.rect.center = self.position

    def draw(self) -> None:
        ContextDisplay.surface.blit(self.image, self.rect)

    def invoke_pressed(self, keys: ScancodeWrapper, key_name: str, callback: Callable[[], None]):
        if any(keys[k] for k in self.keymap[key_name]):
            callback()
