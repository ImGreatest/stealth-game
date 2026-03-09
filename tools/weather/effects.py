from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

import pygame

from core.base import Drawable, Updatable


@dataclass
class WeatherParams:
    intensity: float = 0.0
    speed: float = 1.0
    duration: float = 0.0


class WeatherEffect(ABC):
    def __init__(self):
        self.active = False
        self.params = WeatherParams()
        self.particles = List[Dict[str, Any]] = []

    @abstractmethod
    def start(self):
        pass

    def stop(self):
        self.active = False
        self.params.intensity = 0.0


class Fog(Drawable, Updatable):
    def __init__(self, size: tuple[int, int], color=(255, 255, 255)):
        self.fog_mask = pygame.Surface(size, pygame.SRCALPHA)
        self.fog_color = color

    def draw(self, *args: Any, **kwargs: Any) -> None:
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass
