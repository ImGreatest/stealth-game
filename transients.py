class TransientEffect:
    def __init__(self, lifetime):
        self._lifetime = lifetime
        self._state = False

    def update(self):
        if self._lifetime > 0:
            self._lifetime -= 1

    def is_activate(self):
        return self._state


class PoisoningEffect(TransientEffect):
    def __init__(self, lifetime):
        super().__init__(lifetime)


class BlendingEffect(TransientEffect):
    def __init__(self, lifetime):
        super().__init__(lifetime)


class HealingEffect(TransientEffect):
    def __init__(self, lifetime):
        super().__init__(lifetime)


class PhaseTransientEffect:
    def __init__(self, lifetime):
        self._lifetime = lifetime
