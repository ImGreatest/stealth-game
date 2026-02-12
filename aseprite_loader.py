import json
import pygame


class AsepriteLoader:
    def __init__(self, sprite_path_name: str):
        self.json_path = 'assets/' + sprite_path_name + '.json'
        self.image_path = 'assets/' + sprite_path_name + '.png'
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

        self.rotated_cache = { 0: self.frames }

    def rotate_all_frames(self, angle: float):
        for name, frame_surf in self.frames.items():
            self.frames[name] = pygame.transform.rotate(frame_surf, angle)

    def scale_all_frames(self, size: tuple):
        for name, frame_surf in self.frames.items():
            # Мы используем pygame.transform.scale
            self.frames[name] = pygame.transform.scale(frame_surf, size)

    def scale_by_factor(self, factor: float):
        for name, frame_surf in self.frames.items():
            new_size = (int(frame_surf.get_width() * factor),
                        int(frame_surf.get_height() * factor))
            self.frames[name] = pygame.transform.scale(frame_surf, new_size)

    def draw(self, surface: pygame.Surface, frame_name: str, pos_or_rect, angle: float = 0, flip_x=False):
        if frame_name in self.frames:
            image = self.frames[frame_name]

            if flip_x:
                image = pygame.transform.flip(image, True, False)

            if angle != 0:
                image = pygame.transform.rotate(image, angle)

            if isinstance(pos_or_rect, pygame.Rect):
                new_rect = image.get_rect(center=pos_or_rect.center)
                surface.blit(image, new_rect)
            else:
                surface.blit(image, pos_or_rect)
        else:
            print(f"ERROR, texture not found, with {frame_name}")
