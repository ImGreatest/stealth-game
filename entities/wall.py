from core.base import GameObject
from entities.sprite import Sprite


class Wall(GameObject, Sprite):
    def __init__(self):
        super().__init__()
