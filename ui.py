from abc import ABC
from turtledemo.nim import SCREENWIDTH, SCREENHEIGHT

import pygame

from const import PAUSE_SCREEN_SPECIFICS, MENU_SCREEN_SPECIFICS
from context import Display


class Font:
    def __init__(self, font_size: int = 20):
        self._font_size = font_size
        self.font = pygame.font.SysFont("", self._font_size)


class Text(Font):
    def __init__(self, text: str, position: tuple[int, int], color: tuple[int, int, int] = pygame.Color("white")):
        super().__init__()
        self._text = text
        self._position = position
        self._color = color

        self.surface = self.font.render(self._text, True, self._color)

    def get_rect(self, text_surface):
        rect =  text_surface.get_rect()
        rect.center = self._position
        return rect

    def render(self, screen: pygame.Surface):
        screen.blit(self.surface, self.get_rect(self.surface))


class UserInterface(ABC):
    def __init__(self):
        self.surface_interface = pygame.Surface((800, 600), pygame.SRCALPHA)
        self.surface_interface.fill((240, 245, 255))
        pygame.draw.rect(self.surface_interface, (25, 30, 45, 180), self.surface_interface.get_rect(), border_radius=10)
        pygame.draw.rect(self.surface_interface, (60, 70, 90, 200), self.surface_interface.get_rect(), width=1, border_radius=10)

        self.sections = None

    def screen_blit(self, screen: pygame.Surface):
        screen.blit(self.surface_interface, (0,0))

    def custom_input_controller(self, events: pygame.event.Event):
        pass


class PauseScreen(UserInterface):
    def __init__(self):
        super().__init__()
        self.sections = PAUSE_SCREEN_SPECIFICS

    def draw(self, screen: pygame.Surface):
        self.screen_blit(screen)
        for section in self.sections:
            text = Text(section, (Display.screen.get_width() / 2, Display.screen.get_height() / 2))
            text.render(screen)


class NetGraph(UserInterface):
    def __init__(self):
        super().__init__()


class MenuScreen(UserInterface):
    def __init__(self):
        super().__init__()
        self.sections = MENU_SCREEN_SPECIFICS


class DialogScreen(UserInterface):
    def __init__(self):
        super().__init__()
        self.sections = DialogScreen
