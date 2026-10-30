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

    @property
    def name(self):
        return self.CODE

    def factor(self, weather):
        try:
            return self.TABLE[weather]
        except KeyError:
            raise ValueError(f"unknown weather state: {weather}") from None

    def effective_factor(self, weather):
        f = self.factor(weather)
        return f // 2 if self._durability == 0 else f

    def wear(self):
        if self._durability > 0:
            self._durability -= 1

    def restore(self):
        self._durability = 3

    def snapshot(self):
        return {"code": self.CODE, "durability": self._durability}

    def restore_from(self, state):
        code = state["code"]
        if code != self.CODE:
            raise ValueError("tire snapshot type does not match this tire")
        durability = state["durability"]
        if not 0 <= durability <= 3:
            raise ValueError("tire durability must be between 0 and 3")
        self._durability = durability


class SlickTire(Tire):
    TABLE = {"DRY": 100, "WET": 60}
    CODE = "SLICK"


class RainTire(Tire):
    TABLE = {"DRY": 80, "WET": 90}
    CODE = "RAIN"


def make_tire(code):
    if code == "SLICK":
        return SlickTire()
    if code == "RAIN":
        return RainTire()
    raise ValueError(f"unknown tire type: {code}")
