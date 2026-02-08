from dataclasses import dataclass
from enum import Enum


class TypeItem(Enum):
    weapon = 0
    cloth = 1
    quest_item = 2
    armor = 3
    bullet = 4
    magazine = 5


class Item:
    def __init__(self, item_type: TypeItem):
        self._type = item_type


class TypeWeapon(Enum):
    close_range_weapon = 0
    long_range_weapon = 1
    support_weapon = 2
    heavy_weapon = 3


class Weapon(Item):
    def __init__(self, weapon_type: TypeWeapon, parameters: dict):
        super().__init__(TypeItem.weapon)
        self._weapon_type = weapon_type
        self._parameters = parameters
        self.range = None

    @property
    def range(self):
        return self.range

    @range.setter
    def range(self, value):
        self.range = value


class CloseRangeWeapon(Weapon):
    def __init__(self, parameters: dict):
        super().__init__(TypeWeapon.close_range_weapon, {})


class Knife(CloseRangeWeapon):
    def __init__(self):
        super().__init__({})


class StunGun(CloseRangeWeapon):
    def __init__(self):
        super().__init__({})


class Machete(CloseRangeWeapon):
    def __init__(self):
        super().__init__({})


class Katana(CloseRangeWeapon):
    def __init__(self):
        super().__init__({})


class LongRangeWeapon(Weapon):
    def __init__(self, parameters: dict):
        super().__init__(TypeWeapon.long_range_weapon, {})


class SupportWeapon(Weapon):
    def __init__(self, parameters: dict):
        super().__init__(TypeWeapon.support_weapon, {})


class HeavyWeapon(Weapon):
    def __init__(self, parameters: dict):
        super().__init__(TypeWeapon.heavy_weapon, {})
