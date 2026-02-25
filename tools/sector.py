import numpy as np
import pygame


class Sector:
    def __init__(self, position: pygame.math.Vector2, radius=120, start_angle=0, end_angle=0, color=(255,255,255)):
        self.position = np.array([position.x, position.y], dtype=np.float32)
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.color = color
        self.num_points = 30

        self._angle_factors = np.linspace(0, 1, self.num_points)
        self._cached_points = None
        self._needs_update = True
        self._point_cache = {}

    def _compute_points(self, radius_override=None):
        r = radius_override if radius_override is not None else self.radius
        angles = self.start_angle + self._angle_factors * (self.end_angle - self.start_angle)

        arc_points = self.position + r * np.c_[
            np.cos(angles),
            np.sin(angles)
        ]

        return np.vstack([
            self.position[None, :],
            arc_points,
            self.position[None, :]
        ]).astype(np.int32)

    def set_angles(self, start, end):
        if abs(self.start_angle - start) > 0.001 or abs(self.end_angle - end) > 0.001:
            self.start_angle = start
            self.end_angle = end
            # self._needs_update = True
            # self._point_cache.clear()

    # def finish_update(self):
        # self._needs_update = False

    def get_points(self, radius_override=None):
        r = radius_override if radius_override is not None else self.radius

        # if self._needs_update or r not in self._point_cache:
        points = self._compute_points(r)
        # self._point_cache[r] = [(int(p[0]), int(p[1])) for p in points]
        return points
        # return self._point_cache[r]

    def draw_soft_mask(self, surface, color_override=None):
        draw_color = color_override if color_override else self.color
        layers = 10
        for i in range(layers):
            alpha = int(255 * (i + 1) / layers)

            r = max(1, self.radius - (layers - i) * 3)

            points = self.get_points(radius_override=r)
            points_list = [(int(x), int(y)) for x, y in points]

            final_color = (*draw_color[:3], alpha)
            pygame.draw.polygon(surface, final_color, points_list)

    def update_pos(self, position: pygame.math.Vector2):
        new_pos = np.array([position.x, position.y], dtype=np.float32)
        if not np.array_equal(self.position, new_pos):
            self.position = new_pos
            self._needs_update = True
            self._point_cache.clear()

    def update_angles_from_direction(self, direction_vector, view_angle):
        dir_np = np.array(direction_vector)
        center_angle = np.arctan2(dir_np[1], dir_np[0])
        half_angle = np.radians(view_angle / 2)

        new_start = center_angle - half_angle
        new_end = center_angle + half_angle

        if abs(new_start - self.start_angle) > 0.001 or abs(new_end - self.end_angle) > 0.001:
            self.start_angle = new_start
            self.end_angle = new_end
            # self._needs_update = True
            # self._point_cache.clear()


class SectorRaycast:
    def __init__(self):
        pass
