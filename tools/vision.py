from abc import abstractmethod, ABC

import pygame


class Vision(ABC):
    def __init__(self, color=(255, 255, 255)):
        self.color = color

    def draw_step_gradient(self, mask_surface, base_angle, layers, step_size, max_alpha=255):
        for i in range(layers, 0, -1):
            alpha = int(max_alpha * (1 - i / layers))
            current_range = base_angle + i * step_size
            self._render_layout(mask_surface, current_range, alpha)

    @abstractmethod
    def _render_layout(self, surface, current_range, alpha):
        pass


class AroundVision(Vision):
    def __init__(self, position: pygame.math.Vector2, base_radius=40, color=(255, 180, 50)):
        super().__init__(color)
        self.position = position
        self.base_radius = base_radius

    def _render_layout(self, surface, current_range, alpha):
        pygame.draw.circle(surface,(*self.color, alpha), self.position, int(current_range))


class SectorVision(Vision):
    def __init__(self, sector, color=(255, 240, 150)):
        super().__init__(color)
        self.sector = sector

    def _render_layout(self, surface, current_range, alpha):
        points = self.sector.get_points(radius_override=current_range)
        pygame.draw.polygon(surface, (*self.color, alpha), points)


class LightSource(Vision):
    def __init__(self, position: tuple, color: tuple = (255, 255, 255), light_range=10):
        super().__init__(color)
        self.position = pygame.math.Vector2(position)
        self.light_color = color
        self.light_range = light_range

    def _render_layout(self, surface, current_range, alpha):
        pass
