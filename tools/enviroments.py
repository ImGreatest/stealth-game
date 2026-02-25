import pygame

from core.context import ContextDisplay


class FogOfWar:
    def __init__(self, width, height):
        self.mask = pygame.Surface((width, height), pygame.SRCALPHA)
        self.fog_color = (10, 10, 20)

    def update(self, visions):
        self.mask.fill(self.fog_color)

        for vision in visions:
            vision.draw_to_mask(self.mask)

    def draw(self):
        temp_screen = ContextDisplay.screen.copy()
        ContextDisplay.screen.blit(self.mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
