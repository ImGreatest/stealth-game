import sys

import pygame

from core.const import SCREEN_PADDING
from core.context import ContextDisplay, ContextDt
from core.window import Window
from entities.player import Player
from tools.ui import ScreenControl


class Game:
    def __init__(self):
        pygame.init()
        self.window = Window()
        self.running = True
        self.clock = pygame.time.Clock()

        self.dt = 0.0
        self.fps = 240

        self.player = Player((100, 100))
        self.hud = ScreenControl()

        self.button_surface = pygame.Surface((100, 50))
        self.button_surface.fill((125, 125, 90))
        self.button_rect = self.button_surface.get_rect(center=(200, 100))

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000.0
            ContextDt.dt = self.dt

            self._handle_events()
            self._update(self.dt)
            self._draw()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    print("Da")
                    ContextDisplay.surface.blit(self.screen_control.surface, (0, 0))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        print("da", event.pos)

            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos()) - pygame.math.Vector2(SCREEN_PADDING, SCREEN_PADDING)
            if self.button_rect.collidepoint(mouse_pos):
                self.button_surface.fill((125, 125, 50))
            else:
                self.button_surface.fill((125, 125, 90))

    def _update(self, dt: float):
        self.hud.update(50)
        self.player.update(dt)

    def _draw(self):
        ContextDisplay.surface.fill((20, 20, 10))

        self.player.draw()
        self.hud.draw(ContextDisplay.screen)

        pygame.display.flip()
