from enum import Enum
from typing import Any, List, overload, Union, Dict

import pygame

from core.base import Updatable, Drawable
from core.context import ContextDisplay
from tools.vision import Vision
from tools.weather.effects import WeatherEffect


class MaskType(Enum):
    FOG_OF_WAR = "fog_of_war"
    LIGHTING = "lighting"
    WEATHER_RAIN = "weather_rain"
    WEATHER_FOG = "weather_fog"


MaskTarget = Union[pygame.Surface, None]


# class Environment(Updatable, Drawable):
#     def __init__(self):
#         self.visions: List[Vision] = []
#         self.light_sources: List[LightSource] = []
#         self.weather_effects: Dict[str, WeatherEffect] = {}
#
#         self.fog_of_war_color = (10, 10, 20, 255)
#         self.ambient_light_color = (30, 30, 50, 255)
#
#     def append_vision(self, vision) -> None:
#         self.visions.append(vision)
#
#     def append_light_source(self, light_source) -> None:
#         self.light_sources.append(light_source)
#
#     def append_weather_effect(self, effect, name: str) -> None:
#         self.weather_effects[name] = effect
#
#     def update(self, mask: pygame.Surface, mask_type: MaskType, obstacles: list = None) -> None:
#         if mask_type == MaskType.FOG_OF_WAR:
#             # mask.fill(self.fog_of_war_color)
#
#             for vision in self.visions:
#                 vision.draw_to_mask(mask, obstacles)
#
#             for light in self.light_sources:
#                 light.draw_to_mask(mask, obstacles)
#
#
#     def _update_lighting(self, mask: pygame.Surface, obstacles: list) -> None:
#         mask.fill(self.ambient_light_color)
#
#         for light in self.light_sources:
#             light.draw_to_mask(mask, obstacles)
#
#     def draw(self, mask: pygame.Surface, mask_type: MaskType) -> None:
#         if mask_type == MaskType.LIGHTING:
#             ContextDisplay.screen.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
#         else:
#             ContextDisplay.screen.blit(mask, (0, 0))


class FogOfWar:
    def __init__(self, width, height, color=(10, 10, 20)):
        self.width = width
        self.height = height
        self.mask = pygame.Surface((width, height), pygame.SRCALPHA)
        self.fog_color = (*color, 230)  # Почти непрозрачный туман

    def update(self, visions, light_sources, obstacles) -> None:
        # ВАЖНО: Каждый кадр начинаем с полного тумана
        self.mask.fill(self.fog_color)

        # Применяем все источники видения (они вырезают области в тумане)
        for vision in visions:
            vision.draw_to_mask(self.mask, obstacles)

        # Применяем все источники света (они добавляют цвет в вырезанные области)
        for light in light_sources:
            light.draw_to_mask(self.mask, obstacles)

    def draw(self):
        # Рисуем туман поверх всего
        ContextDisplay.screen.blit(self.mask, (0, 0))
