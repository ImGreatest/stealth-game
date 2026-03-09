from abc import abstractmethod, ABC

import pygame


class Vision(ABC):
    def __init__(self, color=(255, 255, 255)):
        self.color = color

    def draw_step_gradient(self, mask_surface, base_angle, layers, step_size, max_alpha=255):
        for i in range(layers, 0, -1):
            alpha = int(max_alpha * (1 - i / layers))
            current_range = base_angle + i * step_size
            self._render_layout(mask_surface, current_range, alpha)

    @abstractmethod
    def _render_layout(self, surface, current_range, alpha):
        pass

    @abstractmethod
    def draw_to_mask(self, mask: pygame.Surface, obstacles: list):
        pass


class AroundVision(Vision):
    def __init__(self, position: pygame.math.Vector2, base_radius=40, color=(255, 180, 50)):
        super().__init__(color)
        self.position = position
        self.base_radius = base_radius

    def _render_layout(self, surface, current_range, alpha):
        pygame.draw.circle(surface,(*self.color, alpha), self.position, int(current_range))

    def draw_to_mask(self, mask: pygame.Surface, obstacles: list):
        # pygame.draw.circle(surface, (*self.color, alpha), self.position, int(current_range))
        self.draw_step_gradient(mask, self.base_radius, 10, 3, max_alpha=180)


class SectorVision(Vision):
    def __init__(self, sector, color=(255, 240, 150)):
        super().__init__(color)
        self.sector = sector

    def _render_layout(self, surface, current_range, alpha):
        points = self.sector.get_points(radius_override=current_range)
        if len(points) > 2:
            pygame.draw.polygon(surface, (*self.color, alpha), points)

    def draw_to_mask(self, mask: pygame.Surface, obstacles: list):
        self.draw_step_gradient(mask, 250, 8, 2, max_alpha=255)


# class LightSource:
#     def __init__(self, position: tuple, color: tuple = (240, 180, 40), light_range=350, ray_count=160):
#         self.position = pygame.math.Vector2(position)
#         # Немного смягчили цвет: сделали его менее насыщенным и более теплым
#         self.color = color
#         self.light_range = light_range
#         # Увеличили количество лучей для более гладких теней
#         self.ray_count = ray_count
#         self.timer = 0.0
#
#         # ПРЕДЗАГРУЗКА: Создаем мягкий градиентный круг (радиальный градиент)
#         # Это ключ к "приятному" свету. Мы рисуем его один раз.
#         self.gradient_surf = pygame.Surface((light_range * 2, light_range * 2), pygame.SRCALPHA)
#         for r in range(light_range, 0, -2):
#             # Альфа затухает к краям (от 70 до 0)
#             alpha = int(70 * (1 - r / light_range))
#             # Накладываем круги друг на друга, создавая мягкий переход
#             pygame.draw.circle(self.gradient_surf, (*self.color, alpha), (light_range, light_range), r)
#
#     def _cast_ray(self, angle, obstacles):
#         """ Пускает луч и ищет ближайшую точку столкновения """
#         direction = pygame.math.Vector2(1, 0).rotate(angle)
#         ray_end = self.position + direction * self.light_range
#
#         closest_point = ray_end
#         min_dist = self.light_range
#
#         for wall in obstacles:
#             current_walls = wall if isinstance(wall, list) else [wall]
#             for rect in current_walls:
#                 hit = rect.clipline(self.position, ray_end)
#                 if hit:
#                     p1, _ = hit
#                     dist = self.position.distance_to(p1)
#                     if dist < min_dist:
#                         min_dist = dist
#                         closest_point = p1
#         return closest_point
#
#     def draw_to_mask(self, mask_surface: pygame.Surface, obstacles: list):
#         """
#         Мягко прорезает туман и накладывает приятный градиент.
#         """
#
#         # 1. Генерируем точки полигона (ТЕНИ)
#         points = []
#         for i in range(self.ray_count):
#             angle = (360 / self.ray_count) * i
#             points.append(self._cast_ray(angle, obstacles))
#
#         if len(points) > 2:
#             # --- ШАГ 1: Мягкое стирание тумана (BLEND_RGBA_SUB) ---
#             # Создаем слой-"ластик"
#             eraser = pygame.Surface(mask_surface.get_size(), pygame.SRCALPHA)
#
#             # ВАЖНО: Рисуем полигон ТЕНЕЙ, но с альфа-каналом (например, 220),
#             # чтобы края света были чуть размыты.
#             pygame.draw.polygon(eraser, (*self.color, 180), points)
#
#             # Вычитаем из маски FogOfWar
#             mask_surface.blit(eraser, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
#
#             # --- ШАГ 2: Наложение мягкого градиента (ContextDisplay.screen + ADD) ---
#             # Создаем временную поверхность для света
#             # light_overlay = pygame.Surface(mask_surface.get_size(), pygame.SRCALPHA)
#             #
#             # pygame.draw.polygon(light_overlay, (*self.color, 80), points)
#
#             # 2a. Рисуем мягкий градиентный круг на light_overlay в позиции лампы.
#             # Но сначала смещаем, чтобы центр градиента совпал с лампой.
#             grad_rect = self.gradient_surf.get_rect(center=(int(self.position.x), int(self.position.y)))
#             # light_overlay.blit(self.gradient_surf, grad_rect)
#
#             # 3. Накладываем получившийся мягкий свет на экран методом сложения цветов.
#             ContextDisplay.screen.blit(eraser, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
#            int(self.color[0] * 0.8),
