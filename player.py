import abc
import math
from enum import Enum
import pygame

from aseprite_loader import AsepriteLoader
from game_object import GameObject
from sprite import SpriteData
from texture_data import MISSING_TEXTURE


class PlayerDirectionView(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class Player(GameObject):
    def __init__(self, position: tuple):
        super().__init__(position, SpriteData(*MISSING_TEXTURE), (32, 32))
        self.color = pygame.Color("white")

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.direction_view = None

        self.input_controller = InputController(self)
        self.mouse_controller = MouseController(self)
        self.sprite_sheet = AsepriteLoader('missing-texture')

    @property
    def velocity(self):
        return self.velocity_x, self.velocity_y

    @velocity.setter
    def velocity(self, velocity: tuple[float, float]):
        self.velocity_x, self.velocity_y = velocity

    def update(self, events: pygame.event.Event):
        self.input_controller.handle_input(events)
        self.mouse_controller.handle_input(events)


class ControlHandler(abc.ABC):
    @abc.abstractmethod
    def handle_input(self, events: pygame.event.Event):
        pass


class InputController(ControlHandler):
    def __init__(self, player: Player):
        self.player = player

        self.base_speed = 2
        self.sprint_speed = 4

        self.speeds = { False: self.base_speed, True: self.sprint_speed }

    def handle_input(self, events: pygame.event.Event):
        keys = pygame.key.get_pressed()
        self.player.velocity_x, self.player.velocity_y = 0, 0

        speed = self.speeds[keys[pygame.K_LSHIFT]]

        move_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] or keys[pygame.K_d] - keys[pygame.K_a]
        move_y = keys[pygame.K_DOWN] - keys[pygame.K_UP] or keys[pygame.K_s] - keys[pygame.K_w]

        self.player.velocity_x += move_x * speed
        self.player.velocity_y += move_y * speed


class MouseController(ControlHandler):
    def __init__(self, player: Player):
        self.player = player
        self.mouse_pos = (0, 0)
        self.angle = 0
        print(self.mouse_pos)

    def handle_input(self, events: pygame.event.Event):
        keys = pygame.mouse.get_pressed()

        self.mouse_pos = pygame.mouse.get_pos()
        self._calculate_rotation()

        # for event in events:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:
        #             print(self.mouse_pos)

    def _calculate_rotation(self):
        # Разница координат
        dx = self.mouse_pos[0] - self.player.sprite_rect.centerx
        dy = self.mouse_pos[1] - self.player.sprite_rect.centery

        # Вычисляем угол в радианах и переводим в градусы
        # В Pygame ось Y инвертирована, поэтому ставим -dy
        rads = math.atan2(-dy, dx)
        self.angle = math.degrees(rads)
