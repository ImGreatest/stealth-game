from abc import ABC, abstractmethod
from typing import Any

import pygame.font

from core.base import Drawable, Updatable
from core.const import SCREEN_WIDTH, SCREEN_HEIGHT
from core.context import ContextDisplay


class UIElement(ABC):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], anchor: str = "topleft"):
        self.position = position
        self.size = size
        self.anchor = anchor
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(**{self.anchor: self.position})

    def update_position(self, new_pos: tuple[int, int]):
        self.position = new_pos
        self.rect = self.image.get_rect(**{self.anchor: self.position})

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass


class Text(UIElement):
    def __init__(self, text, position, font_size=24, color=(255, 255, 255), anchor="center"):
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(None, font_size)

        # Предварительный рендер для получения размера
        img = self.font.render(self.text, True, self.color)
        super().__init__(position, img.get_size(), anchor)
        self.image = img

    def update_text(self, new_text: str):
        if self.text != new_text:
            self.text = new_text
            self.image = self.font.render(self.text, True, self.color)
            self.rect = self.image.get_rect(**{self.anchor: self.position})

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bar(UIElement):
    def __init__(self, position=(0, 0), size=(40, 6), target_value=100, anchor="center"):
        super().__init__(position, size, anchor)
        self.hp = target_value
        self.max_hp = target_value
        self.colors = {
            "full": (50, 255, 50),
            "medium": (255, 255, 0),
            "low": (255, 0, 0),
            "bg": (40, 40, 40),
            "border": (0, 0, 0),
        }
        self.segment_size = 20  # Каждые 20 единиц HP — разделитель
        self.render_bar()

    def set_values(self, hp, max_hp=None):
        self.hp = max(0, hp)
        if max_hp: self.max_hp = max_hp
        self.render_bar()

    def _get_color(self) -> tuple[int, int, int]:
        ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
        if ratio > 0.6: return self.colors["full"]
        if ratio > 0.2: return self.colors["medium"]
        return self.colors["low"]

    def render_bar(self):
        """Рисует полоску в стиле Factorio на внутреннюю поверхность image"""
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон

        if self.hp <= 0: return

        # 1. Рамка (Border)
        pygame.draw.rect(self.image, self.colors["border"], (0, 0, self.size[0], self.size[1]))

        # 2. Фон (Background) внутри рамки
        inner_rect = (1, 1, self.size[0] - 2, self.size[1] - 2)
        pygame.draw.rect(self.image, self.colors["bg"], inner_rect)

        # 3. Заполнение (Fill)
        ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
        fill_width = int((self.size[0] - 2) * ratio)
        if fill_width > 0:
            fill_rect = (1, 1, fill_width, self.size[1] - 2)
            pygame.draw.rect(self.image, self._get_color(), fill_rect)

        # 4. Сегменты (Разделители как в Factorio)
        num_segments = self.max_hp // self.segment_size
        if num_segments > 1:
            step = (self.size[0] - 2) / num_segments
            for i in range(1, num_segments):
                sep_x = 1 + int(step * i)
                pygame.draw.line(self.image, (0, 0, 0),
                                 (sep_x, 1), (sep_x, self.size[1] - 2), 1)

    def draw(self, surface: pygame.Surface):
        if self.hp > 0:
            surface.blit(self.image, self.rect)


class ScreenControl:
    def __init__(self, size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(0, 0))
        self.visible = False

        self.elements = {
            "title": Text("PAUSE MENU", (size[0] // 2, 50), font_size=40, anchor="center"),
            "health_label": Text("Player Vitals:", (size[0] // 2 - 70, 120), font_size=20, anchor="midright"),
            # Полоска в меню (статичная позиция)
            "hp_bar": Bar((size[0] // 2 + 10, 120), size=(100, 12), anchor="midleft")
        }

    def update(self, player):
        if not self.visible or not player: return
        # Передаем данные игрока в полоску внутри меню
        self.elements["hp_bar"].set_values(player.hp, player.max_hp)

    def draw(self, screen):
        if not self.visible: return
        self.surface.fill((20, 20, 20, 180)) # Затемнение фона
        for el in self.elements.values():
            el.draw(self.surface)
        screen.blit(self.surface, self.rect)
