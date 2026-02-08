import math
from dataclasses import dataclass

from bullet import Bullet, EffectManager
from enemy import Enemy
from player import Player
from wall import Wall


@dataclass
class CollisionObjects:
    player: Player
    walls: list[Wall]
    bullets: list[Bullet]
    enemies: list[Enemy]


class Collision:
    def __init__(self, objects: CollisionObjects, effects: EffectManager):
        self._objects = objects
        self._player = objects.player
        self._walls = objects.walls
        self._bullets = objects.bullets
        self._enemies = objects.enemies
        self._effects = effects

    def handler(self):
        self._player.rect.x += self._player.velocity_x
        self.wall_collision_x()
        self._player.rect.y += self._player.velocity_y
        self.wall_collision_y()

        self.bullet_wall_collision()
        self.bullet_enemy_collision()

    def bullet_enemy_collision(self):
        for bullet in self._bullets[:]:
            if not bullet.visible:
                continue

            for enemy in self._enemies:
                if enemy.rect.colliderect(bullet.rect):
                    zone_name, multiplier = enemy.check_hit(bullet.rect.midright)

                    print(f"Hit ${zone_name} Damage ${multiplier}")

                    if zone_name is None:
                        multiplier = 0.3

                    bullet.visible = False
                    if bullet in self._bullets:
                        self._bullets.remove(bullet)
                    break

    def bullet_wall_collision(self):
        for bullet in self._bullets[:]:
            if not bullet.visible:
                continue

            for wall in self._walls:
                if wall.is_visible() and bullet.rect.colliderect(wall.rect):

                    self._effects.create_impact(
                        *self._effects.calculate_position_wall_impact(bullet),
                        bullet.bullet_angle
                    )
                    bullet.visible = False
                    if bullet in self._bullets:
                        self._bullets.remove(bullet)
                    break

    def wall_collision_x(self):
        for wall in filter(lambda w: w.is_visible(), self._walls):

            if self._player.rect.colliderect(wall.rect):

                if self._player.velocity_x > 0:
                    self._player.rect.right = wall.rect.left

                elif self._player.velocity_x < 0:
                    self._player.rect.left = wall.rect.right

                self._player.velocity_x = 0
                break


    def wall_collision_y(self):
        for wall in filter(lambda w: w.is_visible(), self._walls):

            if self._player.rect.colliderect(wall.rect):

                if self._player.velocity_y > 0:
                    self._player.rect.bottom = wall.rect.top

                elif self._player.velocity_y < 0:
                    self._player.rect.top = wall.rect.bottom

                self._player.velocity_y = 0
                break
