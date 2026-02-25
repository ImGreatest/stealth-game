import abc
import dataclasses
import uuid
from abc import ABC
from typing import Any


@dataclasses.dataclass
class Point:
    x: int
    y: int


class Drawable(ABC):
    @abc.abstractmethod
    def draw(self, *args: Any, **kwargs: Any) -> None:
        pass


class Updatable(ABC):
    @abc.abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class GameObject:
    def __init__(self):
        self._id = uuid.uuid4()

    @property
    def id(self) -> uuid.UUID:
        pass

    @id.setter
    def id(self, new_id: uuid.UUID):
        self._id = new_id

    @id.getter
    def id(self) -> uuid.UUID:
        return self._id
