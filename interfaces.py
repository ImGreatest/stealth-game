from dataclasses import dataclass


@dataclass
class SpriteData:
    """
    Attributes:
        name (str):
        frame_key: (str):
        json_key: (str):
        png_key: (str):
    """
    name: str
    frame_key: str
    json_key: str
    png_key: str


@dataclass
class TransientEffectData:
    lifetime: int
