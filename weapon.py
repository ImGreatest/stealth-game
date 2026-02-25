from entities.sprite import Sprite


class Weapon(Sprite):
    def __init__(self, sprite_name: str, position: tuple, equip_time = 0.5):
        super().__init__(sprite_name, position)

        self.equip_time = equip_time
        self.is_active = False
        self.is_switching = False
        self.switch_timer = 0.0

    def update(self, dt):
        if self.is_switching:
            self.switch_timer -= dt
            if self.switch_timer <= 0:
                self.is_switching = False


class Axe(Weapon):
    def __init__(self, position: tuple):
        super().__init__("axe", position)
        
