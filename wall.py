from enum import Enum

from base import GameObject
from entities import Hitbox, Sprite


class TypeWall(Enum):
    wood = 0
    cement = 1
    rock = 2
    metal = 3


class Wall(GameObject, Sprite, Hitbox):
    def __init__(self, x: int, y: int, size: tuple, type: TypeWall = TypeWall.cement):
        GameObject.__init__(self)
        Sprite.__init__(self, (x, y), None)
        Hitbox.__init__(self, (x, y), size)

        self.x = x
        self.y = y
        self._size = size
        self._type = type
        self._visible = True

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def draw(self):
        super().draw()

    def update(self):
        super().update(self.x, self.y, 0)

    def is_visible(self):
        return self._visible

# class Wall(pygame.sprite.Sprite):
#     def __init__(self, position: tuple, sprite_size: tuple, visible = True):
#         super().__init__()
#         self.sprite_size = sprite_size
#         self.visible = visible
#         self.image = pygame.Surface(sprite_size).convert_alpha()
#         self.rect = self.image.get_rect(topleft=position)
#         self.image.fill(pygame.Color("grey"))
#
#         self.image_loaded = False
#
#     def load_image(self):
#         if not self.image_loaded and pygame.display.get_surface():
#
#             try:
#                 raw_image = pygame.image.load('wall.png').convert_alpha()
#                 self.image = pygame.transform.scale(raw_image, self.sprite_size)
#                 self.image_loaded = True
#             except pygame.error:
#                 print(f'Не найден')
#
#     def update(self, events: pygame.event.Event):
#         pass
#
#     def draw(self, screen: pygame.Surface):
#         # self.load_image()
#         # if self.visible:
#         screen.blit(self.image, self.rect)
#         # pygame.draw.rect(screen, (255, 255, 255), self.rect)
#
#     def is_visible(self):
#         return self.visible
