import json
import pygame


class AsepriteLoader:
    def __init__(self, sprite_path_name: str):
        self.json_path = sprite_path_name + '.json'
        self.image_path = sprite_path_name + '.png'
        with open(self.json_path, 'r') as f:
            data = json.load(f)

        try:
            full_sheet = pygame.image.load(self.image_path).convert_alpha()
        except pygame.error:
            full_sheet = pygame.image.load(self.image_path)
        self.frames = {}

        for name, info in data['frames'].items():
            f = info['frame']
            rect = pygame.Rect(f['x'], f['y'], f['w'], f['h'])
            frame_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
            frame_surf.blit(full_sheet, (0, 0), rect)
            self.frames[name] = frame_surf

    def draw(self, surface: pygame.Surface, frame_name: str, pos: tuple, flip_x=False):
        if frame_name in self.frames:
            image = self.frames[frame_name]
            if flip_x:
                image = pygame.transform.flip(image, True, False)
            surface.blit(image, pos)
        else:
            print(f"ERROR, texture not found, with {frame_name}")
