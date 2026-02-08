from enum import Enum

import pygame

from game_object import GameObject
from sprite import SpriteData
from texture_data import MISSING_TEXTURE


class EnemyState(Enum):
    idle = 0
    suspicion = 1
    in_action = 2
    patrol = 3


class Enemy:
    def __init__(self, position: tuple, sprite_data: SpriteData, health: int):
        # super().__init__(position, sprite_data)
        self._health = health
        self._state = EnemyState.idle
        self.hitboxes = {}

        self.rect = pygame.rect.Rect(position[0], position[1], 32, 32)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health: int):
        self._health = health

    def give_damage(self, damage: int):
        self.health -= damage

    def update_hitboxes(self):
        x, y = self.rect.left, self.rect.top
        w, h = self.rect.width, self.rect.height

        step = h // 5

        self.hitboxes["limbs_top"] = pygame.Rect(x, y, w, step)

        self.hitboxes["torso_top"] = pygame.Rect(x, y + step, w, step)

        self.hitboxes["head"] = pygame.Rect(x, y + 2 * step, w, step)

        self.hitboxes["torso_bottom"] = pygame.Rect(x, y + 3 * step,w, step)

        self.hitboxes["limbs_bottom"] = pygame.Rect(x, y + 4 * step, w, h - 4 * step)


    def check_hit(self, pos):
        if self.hitboxes["head"].collidepoint(pos):
            return "head", 2.0

        if self.hitboxes["torso_top"].collidepoint(pos) or self.hitboxes["torso_bottom"].collidepoint(pos):
            return "torso", 1.0

        if self.rect.collidepoint(pos):
            return "limbs", 0.5

        return None, 0

    def update(self, events: pygame.event.Event):
        self.update_hitboxes()

        part, mult = self.check_hit(pygame.mouse.get_pos())
        if part:
            print(f"Zone {part}, Multiplier {mult}")

    def draw_debug(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.hitboxes["head"], 1)
        pygame.draw.rect(screen, (255, 0, 0), self.hitboxes["torso"], 1)
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)

    def draw(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, (0, 255, 0), self.rect)
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        pygame.draw.rect(screen, (0, 255, 0), self.hitboxes["head"])
        pygame.draw.rect(screen, (255, 0, 0), self.hitboxes["torso_top"])
        pygame.draw.rect(screen, (255, 0, 0), self.hitboxes["torso_bottom"])

class CommonGuardian(Enemy):
    def __init__(self, position: tuple, sprite_data: SpriteData = SpriteData(*MISSING_TEXTURE)):
        super().__init__(position, sprite_data, 100)
