from dataclasses import dataclass


@dataclass
class Permission:
    render_views: int


NO_UI_PERMISSIONS = Permission(0)
DEBUG_PERMISSIONS = Permission(1)


class GameMode:
    def __init__(self, permissions: list[Permission] = DEBUG_PERMISSIONS):
        self._permissions = permissions

    @property
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, permissions: list[Permission]):
        self._permissions = permissions


class DebugMode(GameMode):
    def __init__(self):
        super().__init__([DEBUG_PERMISSIONS])


class NoUIMode(GameMode):
    def __init__(self):
        super().__init__([NO_UI_PERMISSIONS])