import math
import sys
from enum import Enum

import pygame

from core.base import GameObject
from core.const import KEY_MAP, PLAYER_START_STAMINA, PLAYER_START_HEALTH
from tools.sector import Sector
from core.states import IdleState
from entities.hitbox import Hitbox
from entities.sprite import Sprite
from tools.vision import AroundVision, SectorVision


class PlayerDirectionView(Enum):
    RIGHT = 0
    UP_RIGHT = 1
    UP = 2
    UP_LEFT = 3
    LEFT = 4
    DOWN_LEFT = 5
    DOWN = 6
    DOWN_RIGHT = 7


class Player(GameObject, Sprite, Hitbox):
    def __init__(self, position: tuple, size: tuple = (16, 16)):
        GameObject.__init__(self)
        Hitbox.__init__(self, position)
        Sprite.__init__(self, "", position, size)

        self.position = pygame.math.Vector2(position)
        self.size = size

        self.direction_view = None

        self.state = IdleState(self)
        self.controller = Controller(self)
        self.player_vision = PlayerVision(self)

        self.health = PLAYER_START_HEALTH
        self.stamina = PLAYER_START_STAMINA

        self.roll_cooldown_time = 1.0
        self.roll_cooldown_timer = 0.0

        self.health = 100

    def update(self, dt: float, **kwargs):
        if self.roll_cooldown_timer > 0:
            self.roll_cooldown_timer -= dt

        self.controller.handler()

        keys = pygame.key.get_pressed()
        new_state = self.state.handle_input(keys, dt)
        if new_state != self.state:
            self.state = new_state

        self.state.update(dt)

        self.position.x += self.controller.velocity.x * dt
        self.position.y += self.controller.velocity.y * dt

        self.player_vision.update(dt)

        super().update(dt, self.position.x, self.position.y, self.controller.mouse_angle)

    def draw(self):
        super().draw()

        if hasattr(self.state, 'draw'):
            self.state.draw()


class Controller:
    def __init__(self, player: Player):
        self.player = player
        self.keymap = KEY_MAP
        self.velocity = pygame.math.Vector2(0, 0)
        self.mouse_angle = 0

        self.is_running = None
        self.is_crouching = None

    def handler(self):
        self._calculate_rotation()
        self._calculate_movement()
        self._define_direction_view()

    def rebind_key(self, action: str, new_key: str):
        if action in self.keymap:
            self.keymap[action] = new_key

    def _calculate_rotation(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.player.position.x
        dy = mouse_y - self.player.position.y

        rads = math.atan2(-dy, dx)
        self.mouse_angle = math.degrees(rads)

    def _calculate_movement(self):
        keys = pygame.key.get_pressed()
        move = pygame.math.Vector2(0, 0)

        if any(keys[key] for key in self.keymap["move_left"]):
            move.x -= 1

        if any(keys[key] for key in self.keymap["move_right"]):
            move.x += 1

        if any(keys[key] for key in self.keymap["move_up"]):
            move.y -= 1

        if any(keys[key] for key in self.keymap["move_down"]):
            move.y += 1

        if keys[pygame.K_DELETE]:
            pygame.quit()
            sys.exit()

        if move.length() > 0:
            self.velocity = move.normalize()
        else:
            self.velocity.update(0, 0)

    def _define_direction_view(self):
        index = int(((self.mouse_angle + 22.5) % 360) // 45)

        self.player.direction_view = [
            PlayerDirectionView.RIGHT,  # 0 (337.5° - 22.5°)
            PlayerDirectionView.UP_RIGHT,  # 1 (22.5° - 67.5°)
            PlayerDirectionView.UP,  # 2 (67.5° - 112.5°)
            PlayerDirectionView.UP_LEFT,  # 3 (112.5° - 157.5°)
            PlayerDirectionView.LEFT,  # 4 (157.5° - 202.5°)
            PlayerDirectionView.DOWN_LEFT,  # 5 (202.5° - 247.5°)
            PlayerDirectionView.DOWN,  # 6 (247.5° - 292.5°)
            PlayerDirectionView.DOWN_RIGHT  # 7 (292.5° - 337.5°)
        ][index]


class PlayerVision:
    def __init__(self, player: Player):
        self.player = player
        self.current_angle = 0.0
        self.rotation_speed = 5.0
        self.view_angle = 70

        self.sector_geom = Sector(self.player.position, 250, 0, 0)

        self.around_vision = AroundVision(self.player.position, base_radius=20, color=(255, 180, 50))
        self.sector_vision = SectorVision(self.sector_geom)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        target = pygame.math.Vector2(mouse_pos)
        mouse_vec = target - self.player.position

        if mouse_vec.length_squared() > 0:
            import math

            target_angle = math.radians(mouse_vec.as_polar()[1])

            delta = (target_angle - self.current_angle + math.pi) % (2 * math.pi) - math.pi
            self.current_angle += delta * self.rotation_speed * dt

            self.sector_geom.update_pos(self.player.position)

            half_view = math.radians(self.view_angle / 2)
            self.sector_geom.set_angles(self.current_angle - half_view, self.current_angle + half_view)

    def draw_to_mask(self, mask_surface):
        self.around_vision.draw_step_gradient(mask_surface, 20, 10, 3, max_alpha=180)
        # self.sector_vision.draw_step_gradient(mask_surface, 250, 8, -4, max_alpha=255)
        # self.sector_geom.finish_update()
