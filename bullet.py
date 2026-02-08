import math
import random

import pygame


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

        # Рассчитываем вектор движения
        # Угол в радианах, инвертируем Y для Pygame
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


class ImpactParticle:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y

        self.spread = random.uniform(-30, 30)
        self.bounce_angle = math.radians(-(angle + 180 + self.spread))
        self.speed_destroy = random.uniform(2, 5)

        self.is_stuck = False

        self.vel_x = math.cos(self.bounce_angle) * self.speed_destroy
        self.vel_y = math.sin(self.bounce_angle) * self.speed_destroy

        self.lifetime = random.uniform(40, 1200)
        self.fade_speed = random.uniform(0.5, 2.0)
        self.alpha = 255

        self.size = random.randint(2, 3)

        grey_val = random.randint(150, 250)
        self.color = (grey_val, grey_val, grey_val, self.alpha)

        self.friction = random.uniform(0.75, 0.85)

        self.bounce_factor = 0.5

    def update(self):
        if not self.is_stuck:
            self.vel_x *= self.friction
            self.vel_y *= self.friction

            self.x += self.vel_x

            self.y += self.vel_y

            if abs(self.vel_x) < 0.2 and abs(self.vel_y) < 0.2:
                self.is_stuck = True
                # self.lifetime = random.uniform(60, 120)
                self.vel_x = 0
                self.vel_y = 0

        self.lifetime -= self.fade_speed

        self.alpha = max(0, int((self.lifetime / 100) * 255))

        if self.lifetime < 20 and self.size > 0.1:
            self.size -= 0.05

    def draw(self, screen):
        if self.lifetime > 0:
            draw_color = self.color if not self.is_stuck else (100, 100, 100)
            end_x = self.x - self.vel_x * 1.5
            end_y = self.y - self.vel_y * 1.5
            pygame.draw.rect(screen, draw_color, (self.x, self.y, self.size, self.size))
            # pygame.draw.line(screen, self.color, (self.x, self.y), (end_x, end_y), int(self.size))

class EffectManager:
    def __init__(self):
        self.particles = []

        self.decal_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        self.screen_size = (800, 600)

    def create_impact(self, x, y, bullet_angle):
        for _ in range(15):
            self.particles.append(ImpactParticle(x, y, bullet_angle))

    def update(self):
        for p in self.particles[:]:
            p.update()

            if p.is_stuck:
                p.draw(self.decal_surface)
                self.particles.remove(p)

            elif p.lifetime <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        screen.blit(self.decal_surface, (0, 0))

        for p in self.particles:
            p.draw(screen)

    @staticmethod
    def calculate_position_wall_impact(bullet: Bullet):
        rad = math.radians(-bullet.bullet_angle)
        spawn_x = bullet.rect.centerx - math.cos(rad) * 5
        spawn_y = bullet.rect.centery - math.sin(rad) * 5

        return spawn_x, spawn_y
