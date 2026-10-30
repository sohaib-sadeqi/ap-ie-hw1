"""Tires. Each tire type is its own class with its own grip table."""
class Tire:
    TABLE = {"DRY": 100, "WET": 60}
    CODE = "SLICK"

    def __init__(self):
        self._durability = 3

    @property
    def durability(self):
        return self._durability

    def code(self):
        return self.CODE

    def factor(self, weather):
        return self.TABLE[weather]

    def effective_factor(self, weather):
        f = self.factor(weather)
        return f // 2 if self._durability == 0 else f

    def wear(self):
        if self._durability > 0:
            self._durability -= 1

    def restore(self):
        self._durability = 3


class SlickTire(Tire):
    TABLE = {"DRY": 100, "WET": 60}
    CODE = "SLICK"


class RainTire(Tire):
    TABLE = {"DRY": 80, "WET": 90}
    CODE = "RAIN"


def make_tire(code):
    if code == "SLICK":
        return SlickTire()
    return RainTire()