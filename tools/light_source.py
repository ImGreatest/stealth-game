import pygame.math


class LightSource:
    def __init__(self, position=(0, 0), color=(255, 200, 100), light_range=200, ray_count=120):
        self.position = position
        self.color = color
        self.light_range = light_range
        self.ray_count = ray_count

    # def _cast_ray(self):
    #     direction = pygame.math.Vector2(1, 0).rotate(angle)
    #     ray_end = self.position + direction * self.light_range
    #
    #     closest_point = ray_end
    #     min_dist = self.light_range
    #
    #     for wall in obstacles:
    #         current_walls = wall if isinstance(wall, list) else [wall]
    #         for rect in current_walls:
    #             hit = rect.clipline(self.position, ray_end)
    #             if hit:
    #                 p1, _ = hit
    #                 dist = self.position.distance_to(p1)
    #                 if dist < min_dist:
    #                     min_dist = dist
    #                     closest_point = p1
    #     return closest_point


class Lamp(LightSource):
