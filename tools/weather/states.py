from abc import ABC


class WeatherState(ABC):
    def __init__(self, effect: "WeatherEffect"):
        self.effect = effect


class RainState(WeatherState):
    def __init__(self, effect: "WeatherEffect"):
        super().__init__(effect)


class FogState(WeatherState):
    def __init__(self, effect: "WeatherEffect"):
        super().__init__(effect)
