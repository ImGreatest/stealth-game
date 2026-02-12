import math

import pygame

from effects import EffectManager


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position: tuple, velocity: int, angle: int, visible = True):
        super().__init__()
        self._bullet_position = position
        self._bullet_velocity = velocity
        self._bullet_angle = angle
        self.visible = visible

        self.image = pygame.Surface((7, 4), pygame.SRCALPHA)
        self.image.fill((255, 255, 0))

        self.image = pygame.transform.rotate(self.image, self._bullet_angle)
        self.rect = self.image.get_rect(center=self._bullet_position)

        rad = math.radians(-angle)
        self.velocity_x = math.cos(rad) * self._bullet_velocity
        self.velocity_y = math.sin(rad) * self._bullet_velocity

    @property
    def bullet_position(self):
        return self._bullet_position

    @bullet_position.setter
    def bullet_position(self, new_value: tuple):
        self._bullet_position = new_value

    @property
    def bullet_velocity(self):
        return self._bullet_velocity

    @bullet_velocity.setter
    def bullet_velocity(self, new_value: tuple):
        self._bullet_velocity = new_value

    @property
    def bullet_angle(self):
        return self._bullet_angle

    @bullet_angle.setter
    def bullet_angle(self, new_value: int):
        self._bullet_angle = new_value

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if not (0 <= self.rect.x <= 1280 and 0 <= self.rect.y <= 720):
            self.visible = False

    def draw(self, screen: pygame.Surface):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)


class ShootingController:
    def __init__(self):
        self.bullets = []
        self.cooldown = 0
        self.fire_rate = 20
        self.effects = EffectManager()

    def fire(self, pos, angle):
        if self.cooldown <= 0:
            new_bullet = Bullet(pos, 10, angle)
            self.bullets.append(new_bullet)
            self.cooldown = self.fire_rate

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        for bullet in self.bullets[:]:
            bullet.update()

        self.effects.update()

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
        self.effects.draw(screen)
