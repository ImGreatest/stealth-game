import math
import random

import pygame

from base import Updatable, Drawable
from context import Display, DecalDisplay


class ParticleFactory:
    @staticmethod
    def create_bullet_impact(x, y, bullet_angle, count=15):
        return [ImpactParticle(x, y, bullet_angle) for _ in range(count)]

    @staticmethod
    def create_explosion(x, y, count=50):
        return [ExplosionParticle(x, y) for _ in range(count)]


class Particle(Updatable, Drawable):
    def __init__(
            self,
            x: int,
            y: int,
            angle: int,
            speed: int,
            lifetime: int,
            color: tuple,
    ):
        self.x = x
        self.y = y
        self.speed = speed
        self.lifetime = lifetime
        self.color = color
        self.size = random.randint(2, 4)
        self.color = list(color)

        rad = math.radians(angle)
        self.velocity_x = math.cos(rad) * speed
        self.velocity_y = math.sin(rad) * speed

        self.is_stuck = False
        self.friction = None

    def update(self, *args, **kwargs):
        if not self.is_stuck:
            self.velocity_x *= self.friction
            self.velocity_y *= self.friction
            self.x += self.velocity_x
            self.y += self.velocity_y

            if abs(self.velocity_x) < 0.1 and abs(self.velocity_y) < 0.1:
                self.is_stuck = True

        self.lifetime -= 1

    def draw(self, *args, **kwargs):
        if self.lifetime > 0:
            pygame.draw.rect(Display.screen, self.color, (self.x, self.y, self.size, self.size))


class ExplosionParticle(Particle):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.angle = random.randint(0, 360)
        self.speed = random.randint(2, 5)
        self.lifetime = random.randint(30, 50)

        color = (255, random.randint(150, 200), 0)


        super().__init__(x, y, self.angle, self.speed, self.lifetime, color)
        self.friction = 0.92

    def draw(self):
        super().draw()
        if self.lifetime <= 0:
            print("da")

    def update(self):
        super().update()

        if self.color[0] > 60: self.color[0] -= 4
        if self.color[1] > 60: self.color[1] -= 3
        if len(self.color) > 2 and self.color[2] < 60: self.color[2] += 1

        if self.size > 0.5:
            self.size -= 0.1

        if self.lifetime <= 1 or (abs(self.velocity_x) < 0.1 and abs(self.velocity_y) < 0.1):
            self.is_stuck = True
            self.create_decal()

    def create_decal(self):
        if DecalDisplay.decal_surface:
            pygame.draw.circle(DecalDisplay.decal_surface, (20, 20, 20, 150), (int(self.x), int(self.y)), int(self.size * 2))


class ImpactParticle(Particle):
    def __init__(self, x, y, bullet_angle):
        position = (x, y)
        spread = random.uniform(-30, 30)
        angle = int(-(bullet_angle + 180 + spread))
        speed = int(random.uniform(2, 5))
        lifetime = int(random.uniform(40, 100))

        grey = random.randint(150, 250)
        color = (grey, grey, grey)

        super().__init__(position, angle, speed, lifetime, color)
        self.friction = random.uniform(0.75, 0.85)
