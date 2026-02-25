import math
from abc import ABC, abstractmethod

import pygame

from core.const import PLAYER_HEAL_TIME_DURATION, PLAYER_HEAL_SPEED, PLAYER_HEAL_AMOUNT, PLAYER_ROLL_SPEED, \
    PLAYER_ROLL_TIME_DURATION, PLAYER_CROUCH_SPEED, PLAYER_SPRINT_SPEED, PLAYER_WALK_SPEED, PLAYER_ROLL_COOLDOWN
from core.context import ContextDisplay


class PlayerState(ABC):
    def __init__(self, player: "Player"):
        self.player = player

    def is_moving(self, keys):
        actions = ["move_left", "move_right", "move_up", "move_down", "roll", "crouch", "sprint", "crawl"]
        return any(keys[k] for action in actions for k in self.player.controller.keymap[action])

    @abstractmethod
    def handle_input(self, keys, dt):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass


class PlayerWallState(ABC):
    def __init__(self, player: "Player"):
        self.player = player
        self.cling_threshold = 5

    @staticmethod
    def get_nearby_wall(walls):
        for wall in walls:
            # if self.is_near_wall(wall):
                return wall
        return None

    def is_near_wall(self, wall):
        check_distance = self.player.radius + self.cling_threshold

        return

    def get_wall_side(self, wall):
        wall_center_x = wall.x + (wall.cols * wall.v_side) / 2
        wall_center_y = wall.y + (wall.rows * wall.v_side) / 2

        dx = self.player.position.x - wall_center_x
        dy = self.player.position.y - wall_center_y

        if abs(dx) > abs(dy):
            return "EAST" if dx > 0 else "WEST"
        else:
            return "SOUTH" if dy > 0 else "NORTH"

    def get_wall_zone(self, wall):
        rel_pos = wall.get_player_relative_position(self.player.pos)
        return rel_pos


class IdleState(PlayerState):
    def handle_input(self, keys, dt):
        keymap = self.player.controller.keymap

        if any(keys[k] for k in keymap["roll"]):
            return RollState(self.player)

        if any(keys[k] for k in keymap["crouch"]):
            return CrouchState(self.player)

        if any(keys[k] for k in keymap["heal"]):
            return HealState(self.player)

        if self.is_moving(keys):
            return WalkState(self.player)

        return self

    def update(self, dt: float):
        self.player.controller.velocity.update(0, 0)


class WalkState(PlayerState):
    def handle_input(self, keys, dt):
        keymap = self.player.controller.keymap

        if not self.is_moving(keys):
            return IdleState(self.player)

        if any(keys[k] for k in keymap["sprint"]):
            return SprintState(self.player)

        if any(keys[k] for k in keymap["crouch"]):
            return CrouchState(self.player)

        if any(keys[k] for k in keymap["roll"]):
            return RollState(self.player)

        if any(keys[k] for k in keymap["heal"]):
            return HealState(self.player)

        return self

    def update(self, dt: float):
        self.player.controller.velocity *= PLAYER_WALK_SPEED


class SprintState(PlayerState):
    def handle_input(self, keys, dt):
        keymap = self.player.controller.keymap

        if not any(keys[k] for k in keymap["sprint"]):
            return WalkState(self.player)

        if any(keys[k] for k in keymap["roll"]):
            return RollState(self.player)

        if any(keys[k] for k in keymap["heal"]):
            return HealState(self.player)

        if not self.is_moving(keys):
            return IdleState(self.player)

        return self

    def update(self, dt: float):
        self.player.controller.velocity *= PLAYER_SPRINT_SPEED


class CrouchState(PlayerState):
    def handle_input(self, keys, dt):
        keymap = self.player.controller.keymap

        if not any(keys[k] for k in keymap["crouch"]):
            return IdleState(self.player) if not self.is_moving(keys) else WalkState(self.player)

        if any(keys[k] for k in keymap["roll"]):
            return RollState(self.player)

        if any(keys[k] for k in keymap["heal"]):
            return HealState(self.player)

        return self

    def update(self, dt: float):
        # self.cooldown -= dt
        self.player.controller.velocity *= PLAYER_CROUCH_SPEED
        self.player.mask_surface = self.player.mask.to_surface(
            setcolor=(0, 255, 255),
            unsetcolor=(0, 0, 0, 0)
        )

    def __del__(self):
        self.player.mask_surface = self.player.mask.to_surface(
            setcolor=(0, 0, 0, 0),
            unsetcolor=(0, 0, 0, 0)
        )


class RollState(PlayerState):
    def __init__(self, player: "Player"):
        super().__init__(player)
        self.timer = PLAYER_ROLL_TIME_DURATION

        vel = self.player.controller.velocity
        self.roll_direction = pygame.math.Vector2(vel.x, vel.y)

        if self.roll_direction.length() == 0:
            angle_rad = math.radians(self.player.controller.mouse_angle)
            self.roll_direction = pygame.math.Vector2(math.cos(angle_rad), math.sin(angle_rad))
        else:
            self.roll_direction = self.roll_direction.normalize()

    def handle_input(self, keys, dt):
        if self.timer <= 0:
            if any(keys[k] for k in self.player.controller.keymap["crouch"]):
                return CrouchState(self.player)
            return WalkState(self.player) if self.is_moving(keys) else IdleState(self.player)

        return self

    def update(self, dt: float):
        self.timer -= dt
        self.player.controller.velocity = self.roll_direction * PLAYER_ROLL_SPEED
        temp_mask = self.player.mask.to_surface(
            setcolor=(150, 150, 150),
            unsetcolor=(0, 0, 0, 0)
        )
        print("da")
        temp_mask.set_alpha(128)
        self.player.mask_surface = temp_mask


class HealState(PlayerState):
    def __init__(self, player: "Player"):
        super().__init__(player)
        self.timer = PLAYER_HEAL_TIME_DURATION

        self.draw()

    def handle_input(self, keys, dt):
        keymap = self.player.controller.keymap

        if self.timer <= 0:
            if hasattr(self.player, 'heal'):
                self.player.heal(PLAYER_HEAL_AMOUNT)
            return WalkState(self.player) if self.is_moving(keys) else IdleState(self.player)

        if any(keys[k] for k in keymap["roll"]):
            return RollState(self.player)

        return self

    def update(self, dt: float):
        self.timer -= dt

        if self.is_moving(pygame.key.get_pressed()):
            self.player.controller.velocity *= PLAYER_HEAL_SPEED
        else:
            self.player.controller.velocity.update(0, 0)

        self.player.mask_surface = self.player.mask.to_surface(
            setcolor=(0, 255, 0),
            unsetcolor=(0, 0, 0, 0)
        )

        alpha = int(150 + 50 * math.sin(pygame.time.get_ticks() * 0.01))
        self.player.mask_surface.set_alpha(alpha)

    def draw(self):
        ratio = self.timer / PLAYER_HEAL_TIME_DURATION
        bar_rect = pygame.Rect(self.player.hitbox_rect.centerx - 20,
                               self.player.hitbox_rect.top - 10, 40 * (1 - ratio), 4)
        pygame.draw.rect(ContextDisplay.screen, (0, 255, 0), bar_rect)


class CrawlState(PlayerState):
    def __init__(self, player: "Player"):
        super().__init__(player)

    def handle_input(self, keys, dt):
        keymap = self.player.controller.keymap

        if not any(keys[k] for k in keymap["crawl"]):
            return IdleState(self.player) if not self.is_moving(keys) else CrouchState(self.player)

        if any(keys[k] for k in self.player.controller.keymap["crouch"]):
            return CrouchState(self.player)

        return self


    def update(self, dt: float):
        self.player.mask_surface = self.player.mask.to_surface(
            set_color=(0, 255, 122),
            unsetcolor=(0, 0, 0, 0)
        )

    def __del__(self):
        self.player.mask_surface = self.player.mask.to_surface(
            setcolor=(0, 0, 0, 0),
            unsetcolor=(0, 0, 0, 0)
        )

class ClingState(PlayerState):
    def __init__(self, player: "Player"):
        super().__init__(player)

    def handle_input(self, keys, dt):
        pass

    def update(self, dt: float):
        pass
