import pygame


class Obstacle(pygame.sprite.Sprite):
    obstacles = pygame.sprite.Group()

    def __init__(self, position, size, height=100):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=position)
        # self.rect = pygame.Rect(position, size)
        self.height = height
        Obstacle.obstacles.add(self)

    @classmethod
    def get_obstacles(cls):
        return [sprite.rect for sprite in cls.obstacles]

    def deactivate(self):
        self.kill()
