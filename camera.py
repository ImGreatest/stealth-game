import pygame
from event_bus import EventBus


class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.width = screen_width
        self.height = screen_height
        self.offset = pygame.Vector2(0, 0)

        self.zoom_scale = 1.0
        self.zoom_min = 0.2
        self.zoom_max = 3.0

        EventBus.subscribe(pygame.MOUSEWHEEL, self.handle_zoom)

    def update(self, target_rect):
        """Set center camera on target"""
        self.offset.x = target_rect.centerx - self.width // 2
        self.offset.y = target_rect.centery - self.width // 2

    def apply_point(self, x, y):
        """Превращает мировые координаты в экранные с учетом зума"""
        rel_x = x - (self.offset.x + self.width // 2)
        rel_y = y - (self.offset.y + self.height // 2)

        screen_x = (rel_x * self.zoom_scale) +  self.width // 2
        screen_y = (rel_y * self.zoom_scale) + self.height // 2

        return screen_x, screen_y

    def apply_rect(self, rect: pygame.Rect):
        """Возвращает Rect, масштабированный и сдвинутый для отрисовки"""
        x, y = self.apply_point(rect.x, rect.y)
        w, h = rect.width * self.zoom_scale, rect.height * self.zoom_scale

        return pygame.Rect(x, y, w, h)

    def screen_to_world(self, screen_pos):
        """Конвертирует клик мыши в мировые координаты с учетом зума"""
        rel_x = (screen_pos[0] - self.width // 2) / self.zoom_scale
        rel_y = (screen_pos[1] - self.height // 2) / self.zoom_scale

        world_x = rel_x + (self.offset.x + self.width // 2)
        world_y = rel_y + (self.offset.y + self.height // 2)

        return pygame.Vector2(world_x, world_y)

    def handle_zoom(self, event):
        self.zoom_scale += event.y * 0.1
        self.zoom_scale = max(self.zoom_min, min(self.zoom_max, self.zoom_scale))
