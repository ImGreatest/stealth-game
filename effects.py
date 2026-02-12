import random

import pygame

from context import Display, DecalDisplay
from particles import Particle, ParticleFactory


class EffectManager:
    def __init__(self):
        self.particles = []

        self.decal_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
        DecalDisplay.decal_surface = self.decal_surface

    def add_impact(self, bullet):
        spawn_pos = Particle.calculate_impact_point(bullet)
        new_particles = ParticleFactory.create_bullet_impact(spawn_pos, bullet.bullet_angle)
        self.particles.extend(new_particles)

    def create_explosion_effect(self, x, y):
        if DecalDisplay.decal_surface:
            crater_radius = random.randint(20, 35)

            pygame.draw.circle(
                DecalDisplay.decal_surface,
                (10, 10, 10, 180),
                (int(x), int(y)),
                crater_radius,
            )

            pygame.draw.circle(
                DecalDisplay.decal_surface,
                (30, 30, 30, 150),
                (int(x), int(y)),
                crater_radius // 2
            )

        new_particles = ParticleFactory.create_explosion(x, y)
        self.particles.extend(new_particles)


    def update(self):
        for p in self.particles[:]:
            p.update()

            if p.is_stuck:
                p.draw()
                self.particles.remove(p)

            elif p.lifetime <= 0:
                if hasattr(p, 'create_decal'):
                    p.create_decal()
                self.particles.remove(p)

    def draw(self):
        Display.screen.blit(self.decal_surface, (0, 0))

        for p in self.particles:
            p.draw()
