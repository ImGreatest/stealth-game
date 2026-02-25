import pygame

KEY_MAP = {
    "move_up": [pygame.K_UP, pygame.K_w],
    "move_down": [pygame.K_DOWN, pygame.K_s],
    "move_left": [pygame.K_LEFT, pygame.K_a],
    "move_right": [pygame.K_RIGHT, pygame.K_d],
    "crouch": [pygame.K_c, pygame.K_LCTRL],
    "crawl": [pygame.K_v],
    "sprint": [pygame.K_LSHIFT],
    "roll": [pygame.K_x],
    "heal": [pygame.K_h],
    "action": [pygame.K_e],
}

PLAYER_START_HEALTH = 100
PLAYER_START_STAMINA = 100

PLAYER_WALK_SPEED = 150
PLAYER_SPRINT_SPEED = PLAYER_WALK_SPEED * 2
PLAYER_CROUCH_SPEED = PLAYER_WALK_SPEED / 2
PLAYER_CRAWL_SPEED = PLAYER_CROUCH_SPEED * 4

PLAYER_ROLL_SPEED = 150 * 3
PLAYER_ROLL_TIME_DURATION = 0.4
PLAYER_ROLL_COOLDOWN = 0.4

PLAYER_HEAL_TIME_DURATION = 2.0
PLAYER_HEAL_AMOUNT = 20
PLAYER_HEAL_SPEED = 50
