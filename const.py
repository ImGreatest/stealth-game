from interfaces import SpriteData, TransientEffectData
from transients import TransientEffect

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PAUSE_SCREEN_SPECIFICS = {
    "pause"
}

PAUSE_MENU_SCREEN_SPECIFICS = {
    "restart",
    "settings",
    "save",
    "exit",
}

MENU_SCREEN_SPECIFICS = {
    "start",
    "settings",
    "exit",
}

SETTINGS_SCREEN_SPECIFICS = {
    "exit"
}

DIALOG_SCREEN_SPECIFICS = {
    "yes",
    "no"
}

MISSING_TEXTURE = SpriteData(
    name="missing-texture",
    frame_key="missing-texture.aseprite",
    json_key="missing-texture.json",
    png_key="missing-texture.png",
)

RED_SLATE_CRACKED = SpriteData(
    name="red-slate-cracked",
    frame_key="red-slate-cracked.aseprite",
    json_key="red-slate-cracked.json",
    png_key="red-slate-cracked.png",
)

PLAYER_DATA = SpriteData(
    name="",
    frame_key="",
    json_key="",
    png_key="",
)

POISING_EFFECT_LIFETIME = TransientEffectData(50)
BLENDING_EFFECT_LIFETIME = TransientEffectData(100)
HEALING_EFFECT_LIFETIME = TransientEffectData(25)
