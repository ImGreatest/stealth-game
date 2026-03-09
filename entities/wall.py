from core.base import Drawable, Updatable
from tools.obstacle import Obstacle


class Wall(Obstacle, Drawable, Updatable):
    def __init__(self):
        super().__init__()
