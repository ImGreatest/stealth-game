from abc import ABC, abstractmethod

import pygame.font

from core.base import Drawable, Updatable
from core.context import ContextDisplay


class UIElement(ABC):
    def __init__(self, position: tuple[int, int] = (0, 0), size: tuple[int, int] = (0, 0)):
        self._position = position
        self._size = size

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, value: tuple[int, int]):
        self._position = value
        self._on_position_changed()

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value
        self._on_size_changed()

    def _on_position_changed(self):
        pass

    def _on_size_changed(self):
        pass

    @abstractmethod
    def frame(self, *args, **kwargs):
        pass


class Text(UIElement, Drawable, Updatable):
    def __init__(
            self,
            position: tuple[int, int],
            text: str = "",
            color: tuple[int, int, int] = (255, 255, 255),
            font_size = 24,
            font_path = None,
            anchor: str = "center",
    ):
        super().__init__(position, (0, 0))
        self._text = text
        self._color = color
        self._anchor = anchor
        self._font_size = font_size
        self._font_path = font_path
        self._font = None
        self._text_surface = None
        self._text_rect = None
        self._init_font()
        self._render_text()

        self.font = pygame.font.Font("./assets/Font.ttf", 24)
        self._render_text()

    def _init_font(self):
        try:
            if self._font_path:
                self._font = pygame.font.Font(self._font_path, self._font_size)
            else:
                self._font = pygame.font.Font(None, self._font_size)
        except FileNotFoundError:
            self._font = pygame.font.SysFont(None, self._font_size)

    def _render_text(self):
        self._text_surface = self._font.render(self._text, True, self._color)
        self._size = self._text_surface.get_size()
        self._update_rect_position()

    def _update_rect_position(self):
        if not self._text_surface:
            return
        self._text_rect = self._text_surface.get_rect()
        if self._anchor == "center":
            self._text_rect.center = self._position
        elif self._anchor == "left":
            self._text_rect.midleft = self._position
        elif self._anchor == "right":
            self._text_rect.midright = self._position
        else:
            self._text_rect.topleft = self._position

    def _on_position_changed(self):
        self._update_rect_position()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if self._text != value:
            self._text = value
            self._render_text()

    @property
    def color(self) -> tuple[int, int, int]:
        return self._color

    @color.setter
    def color(self, value: tuple[int, int, int]):
        if self._color != value:
            self._color = value
            self._render_text()

    def draw(self):
        if self._text_surface:
            ContextDisplay.screen.blit(self._text_surface, self._text_rect)

    def update(self, *args, **kwargs):
        pass

    def frame(self, *args, **kwargs):
        if args:
            self.text = str(args[0])
        elif 'text' in kwargs:
            self.text = str(kwargs['text'])
        self.update()
        self.draw()


class StaticText(Text):
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)


class DynamicText(Text):
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)


class Bar(UIElement, Drawable, Updatable):
    def __init__(self):
        self.width = 40
        self.height = 6
        self.x, self.y = 0, 0
        self.hp = 0
        self.max_hp = 100
        self.colors = {
            "full": (50, 255, 50),
            "medium": (255, 255, 0),
            "low": (255, 0, 0),
            "bg": (40, 40, 40),
            "border": (0, 0, 0),
        }
        super().__init__()

    def set_position(self, position: tuple[int, int]):
        self.x, self.y = position

    def set_values(self, hp: int, max_hp: int = None):
        self.hp = min(hp, self.max_hp if max_hp is None else max_hp)
        if max_hp is not None:
            self.max_hp = max_hp

    def _get_color(self) -> tuple[int, int, int]:
        ratio = self.hp / self.max_hp
        if ratio > 0.6:
            return self.colors["full"]
        elif ratio > 0.2:
            return self.colors["medium"]
        else:
            return self.colors["low"]

    def draw(self):
        if self.hp <= 0:
            return

        left = self.x - self.width // 2
        bar_rect = pygame.Rect(left, self.y, self.width, self.height)
        fill_width = int(self.width * (self.hp / self.max_hp))
        fill_rect = pygame.Rect(left, self.y, fill_width, self.height)

        pygame.draw.rect(ContextDisplay.screen, self.colors["border"], bar_rect.inflate(2, 2))
        pygame.draw.rect(ContextDisplay.screen, self.colors["bg"], bar_rect)
        pygame.draw.rect(ContextDisplay.screen, self._get_color(), fill_rect)

        segment_size = 20
        num_segments = self.max_hp // segment_size
        if num_segments > 1:
            step = self.width / num_segments
            for i in range(1, num_segments):
                sep_x = left + int(step * i)
                pygame.draw.line(
                    ContextDisplay.screen, (0, 0, 0),
                    (sep_x, self.y), (sep_x, self.y + self.height - 1), 1
                )

    def frame(self, position: tuple[int, int], hp: int, max_hp=100, **kwargs):
        self.x, self.y = position
        self.y = self.y - 16 - 5
        self.x = self.x + 0 // 2
        self.set_values(hp, max_hp)
        self.draw()

    def update(self, hp):
        self.hp = hp


class Screen:
    def __init__(
            self,
            ui_objects: list[UIElement],
            color: tuple[int, int, int] = (10, 10, 10),
            surface_position: tuple[int, int] = (0, 0),
            surface_size: tuple[int, int] = (0, 0),
    ):
        self.ui_objects = ui_objects
        self.color_theme = color
        self._surface_position = surface_position

        self.surface = pygame.Surface(surface_size)
        self.surface.fill(self.color_theme)

    def blit(self, *args, **kwargs):
        pass


class UIScreen(Screen):
    def __init__(self, player: "Player"):
        self.player = player
        objects = [
            Text((10, 20),  anchor="left"),
            Bar()
        ]
        super().__init__(objects, color=(10, 25, 10))

    def blit(self, *args, **kwargs):
        ContextDisplay.screen.blit(self.surface, self._surface_position)

        for obj in self.ui_objects:
            if isinstance(obj, Bar):
                obj.frame(self.player.position, self.player.health)  # передай данные
            elif isinstance(obj, Text):
                if args:
                    text = str(args[0])
                    obj.frame(text=text)
                elif kwargs.get('text') is not None:
                    text = str(kwargs.get('text'))
                    obj.frame(text=text)
            else:
                obj.frame()
