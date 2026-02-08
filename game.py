import pygame

from bullet import ShootingController
from collision import Collision, CollisionObjects
from enemy import CommonGuardian
from player import Player
from sprite import Sprite, SpriteData
from texture_data import RED_SLATE_CRACKED
from wall import Wall


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.player = Player((100, 300))
        self.sprite = Sprite((100, 400), SpriteData(*RED_SLATE_CRACKED))
        self.wall = Wall((300, 300), (50, 100))
        self.common_guardian = CommonGuardian((400, 100))

        self.wall_sprites = pygame.sprite.Group()
        self.wall_sprites.add(self.wall)

        self.shooting_system = ShootingController()
        self.collision_handler = Collision(
            objects=CollisionObjects(self.player, [self.wall], self.shooting_system.bullets, [self.common_guardian]),
            effects=self.shooting_system.effects
        )

        self.pause_status = False

    def tick(self):
        self.clock.tick(self.fps)

    def draw(self, screen: pygame.Surface):

        screen.fill((20, 20, 40))
        for wall in self.wall_sprites:
            wall.draw(screen)

        self.common_guardian.draw(screen)

        self.sprite.draw_sprite(screen)

        self.shooting_system.draw(screen)

        self.player.draw(screen)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_status = not self.pause_status

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = self.player.sprite_rect.center
                    angle = self.player.mouse_controller.angle
                    self.shooting_system.fire(pos, angle)

        self.shooting_system.update()

        for wall in self.wall_sprites:
            wall.update(events)

        self.common_guardian.update(events)

        self.collision_handler.handler()
        self.player.update(events)