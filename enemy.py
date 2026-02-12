from enum import Enum

from base import GameObject
from entities import Hitbox, Sprite


class EnemyState(Enum):
    idle = 0
    suspicion = 1
    in_action = 2
    patrol = 3


class Enemy(GameObject, Sprite, Hitbox):
    def __init__(self, position: tuple, size: tuple = (16, 16)):
        GameObject.__init__(self)
        Sprite.__init__(self, position, None)
        Hitbox.__init__(self, position, size)

        self._position = position
        self._size = size

        self.velocity_x, self.velocity_y = 0, 0
        self.direction_view = None

    def update(self):
        super().update(self._position[0], self._position[1], 0)

    def draw(self):
        super().draw()
