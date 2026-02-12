import uuid
from abc import abstractmethod, ABC


class Drawable(ABC):
    @abstractmethod
    def draw(self, *args, **kwargs):
        pass


class Updatable(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class GameObject:
    def __init__(self):
        self._id = uuid.uuid4()

    def get_id(self):
        return self._id
