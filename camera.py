import pygame

from const import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self):
        self.camera_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.speed = 0.1

    def apply(self, entity_rect: pygame.Rect):
        return entity_rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_point(self, point):
        return point[0] - self.camera_rect.x, point[1] - self.camera_rect.y

    def update(self, target_rect: pygame.Rect):
        target_x = target_rect.centerx - int(SCREEN_WIDTH / 2)
        target_y = target_rect.centery - int(SCREEN_HEIGHT / 2)

        self.camera_rect.x += (target_x - self.camera_rect.x) * self.speed
        self.camera_rect.y += (target_y - self.camera_rect.y) * self.speed
