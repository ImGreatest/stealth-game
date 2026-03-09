import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any


class Drawable(ABC):
    @abstractmethod
    def draw(self, *args: Any, **kwargs: Any) -> None:
        pass


class Updatable(ABC):
    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        pass


class TagMeta:
    _registry = defaultdict(list)

    @classmethod
    def register(cls, tag_name, instance):
        cls._registry[tag_name].append(instance)

    @classmethod
    def unregister(cls, tag_name, instance):
        if instance in cls._registry[tag_name]:
            cls._registry[tag_name].remove(instance)

    @classmethod
    def find_all(cls, tag_class):
        name = tag_class if isinstance(tag_class, str) else tag_class.__name__

        return cls._registry.get(name, [])

    @classmethod
    def find_first(cls, tag_class):
        results = cls.find_all(tag_class)

        return results[0] if results else None


class Tag:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.tag_name = cls.__name__

    def __init__(self):
        self.instance_id = uuid.uuid4().hex[:6]
        TagMeta.register(self.tag_name, self)

    def destroy(self):
        TagMeta.unregister(self.tag_name, self)
