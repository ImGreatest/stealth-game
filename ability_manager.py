class Ability:
    def __init__(self):
        pass


class AbilityManager:
    def __init__(self, owner):
        self.owner = owner
        self.abilities = {}

    def add_ability(self, key: str, ability: Ability):
        self.abilities[key] = ability

    def update(self, dt: float):
        for ability in self.abilities.values():
            ability.update(dt)
