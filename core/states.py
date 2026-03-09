from abc import ABC

import pygame
from pygame.key import ScancodeWrapper

from core.const import PLAYER_HEAL_TIME_DURATION, PLAYER_HEAL_SPEED, PLAYER_HEAL_AMOUNT, PLAYER_ROLL_SPEED, \
    PLAYER_ROLL_TIME_DURATION, PLAYER_CROUCH_SPEED, PLAYER_SPRINT_SPEED, PLAYER_WALK_SPEED, PLAYER_ROLL_COOLDOWN, \
    PLAYER_LIE_SPEED


class PlayerState(ABC):
    def __init__(self, player: "Player"):
        self.player = player

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        return self

    def update(self, dt: float):
        pass

    def is_moving(self, keys: ScancodeWrapper):
        actions = ["move_left", "move_right", "move_up", "move_down", "roll", "crouch", "sprint", "lie"]
        return any(keys[k] for action in actions for k in self.player.keymap[action])


class IdleState(PlayerState):
    def __enter__(self):
        self.player.current_speed = 0.0
        self.player.height = 1.8
        self.player.color = pygame.Color("green")
        self.player.image.fill(self.player.color)

        return self

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        if any(keys[k] for k in self.player.keymap["roll"]):
            return RollState(self.player)

        if any(keys[k] for k in self.player.keymap["heal"]):
            return HealState(self.player)

        if any(keys[k] for k in self.player.keymap["crouch"]):
            return CrouchState(self.player)

        if any(keys[k] for k in self.player.keymap["lie"]):
            return LyingState(self.player)

        if self.is_moving(keys):
            return WalkState(self.player)

        return self


class WalkState(PlayerState):
    def __enter__(self):
        self.player.current_speed = PLAYER_WALK_SPEED
        self.player.height = 1.8
        self.player.color = pygame.Color("white")
        self.player.image.fill(self.player.color)

        return self

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        if any(keys[k] for k in self.player.keymap["roll"]):
            return RollState(self.player)

        if any(keys[k] for k in self.player.keymap["heal"]):
            return HealState(self.player)

        if any(keys[k] for k in self.player.keymap["crouch"]):
            return CrouchState(self.player)

        if any(keys[k] for k in self.player.keymap["lie"]):
            return LyingState(self.player)

        if not self.is_moving(keys):
            return IdleState(self.player)

        if any(keys[k] for k in self.player.keymap["sprint"]):
            return SprintState(self.player)

        return self

    def update(self, dt: float):
        self.player.current_speed = PLAYER_WALK_SPEED


class SprintState(PlayerState):
    def __enter__(self):
        self.player.current_speed = PLAYER_SPRINT_SPEED
        self.player.color = pygame.Color("cyan")
        self.player.image.fill(self.player.color)

        return self

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        if any(keys[k] for k in self.player.keymap["heal"]):
            return HealState(self.player)

        if any(keys[k] for k in self.player.keymap["roll"]):
            return RollState(self.player)

        if not any(keys[k] for k in self.player.keymap["sprint"]):
            return WalkState(self.player)

        if not self.is_moving(keys):
            return IdleState(self.player)

        return self


class CrouchState(PlayerState):
    def __enter__(self):
        self.player.current_speed = PLAYER_CROUCH_SPEED
        self.player.height = 1.0
        self.player.color = pygame.Color("yellow")
        self.player.image.fill(self.player.color)

        self.player.mask_surface = self.player.mask.to_surface(setcolor=(0, 255, 255), unsetcolor=(0, 0, 0, 0))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.player.mask_surface = None

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        if not any(keys[k] for k in self.player.keymap["crouch"]):
            return WalkState(self.player) if self.is_moving(keys) else IdleState(self.player)

        if any(keys[k] for k in self.player.keymap["roll"]):
            return RollState(self.player)

        return self


class LyingState(PlayerState):
    def __enter__(self):
        self.player.current_speed = PLAYER_LIE_SPEED
        self.player.height = 0.5
        self.player.color = pygame.Color("red")
        self.player.image.fill(self.player.color)

        return self

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        if any(keys[k] for k in self.player.keymap["heal"]):
            return HealState(self.player)

        if any(keys[k] for k in self.player.keymap["crouch"]):
            return CrouchState(self.player)

        if any(keys[k] for k in self.player.keymap["lie"]):
            if self.is_moving(keys):
                return WalkState(self.player)
            else:
                return IdleState(self.player)

        return self


class RollState(PlayerState):
    def __init__(self, player: "Player"):
        super().__init__(player)
        self.timer = PLAYER_ROLL_TIME_DURATION

        vel = self.player.velocity
        if vel.length() == 0:
            import math
            angle = math.radians(self.player.mouse_angle if self.player.mouse_angle else 0)
            self.roll_dir = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        else:
            self.roll_dir = vel.normalize()

    def __enter__(self):
        self.player.is_invulnerable = True
        self.player.current_speed = PLAYER_ROLL_SPEED
        self.player.color = pygame.Color("purple")
        self.player.image.fill(self.player.color)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.player.is_invulnerable = False
        self.player.mask_surface = None

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        if self.timer <= 0:
            return WalkState(self.player) if self.is_moving(keys) else IdleState(self.player)

        return self

    def update(self, dt: float):
        self.timer -= dt
        self.player.velocity = self.roll_dir * PLAYER_ROLL_SPEED
        self.player.mask_surface = self.player.mask.to_surface(setcolor=(150, 150, 150), unsetcolor=(0, 0, 0, 0))
        self.player.mask_surface.set_alpha(128)


class HealState(PlayerState):
    def __init__(self, player: "Player"):
        super().__init__(player)
        self.timer = PLAYER_HEAL_TIME_DURATION

    def __enter__(self):
        self.player.can_use_weapons = False
        self.player.current_speed = PLAYER_HEAL_SPEED
        self.player.mask_surface = self.player.mask.to_surface(
            setcolor=(0, 255, 0),
            unsetcolor=(0, 0, 0, 0),
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.player.can_use_weapons = True
        self.player.mask_surface = None

    def handle_input(self, keys: ScancodeWrapper, dt: float) -> "PlayerState":
        if self.timer <= 0:
            if hasattr(self.player, 'heal'):
                self.player.heal(PLAYER_HEAL_AMOUNT)
            return WalkState(self.player) if self.is_moving(keys) else IdleState(self.player)
        if any(keys[k] for k in self.player.keymap["roll"]): return RollState(self.player)

        return self

    def update(self, dt: float):
        self.timer -= dt
        import math
        if self.player.mask:
            alpha = int(150 + 50 * math.sin(pygame.time.get_ticks() * 0.01))
            self.player.mask.set_alpha(alpha)
