import pygame


class Render:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.camera_offset = pygame.Vector2(0, 0)

    def update_camera(self, target_rect):
        self.camera_offset = target_rect.centerx - self.screen.get_width() // 2
        self.camera_offset = target_rect.centery - self.screen.get_height() // 2

    def render_object(self, obj):
        self.screen.blit(obj.image, obj.rect.topleft - self.camera_offset)
