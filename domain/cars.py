
from .car import Car
from .engine import Engine
from .turbo import TurboCharger, OverboostTurbo


class VelocityCar(Car):
    def __init__(self):
        super().__init__(
            name="Velocity",
            max_health=80,
            engine=Engine(100),
            turbo=TurboCharger(cost=5, boost=20),
            attack=25,
            resistance=5,
            repair_amount=30,
            repair_quota=1,
        )

    def ability_name(self):
        return "Last Stand"

    def modify_move_base(self, base):
        if self._health < 32:
            return (base * 6) // 5
        return base


class BlazeCar(Car):
    def __init__(self):
        super().__init__(
            name="Blaze",
            max_health=90,
            engine=Engine(80),
            turbo=OverboostTurbo(),
            attack=20,
            resistance=10,
            repair_amount=20,
            repair_quota=2,
        )

    def ability_name(self):
        return "Overboost"


class TitanCar(Car):
    def __init__(self):
        super().__init__(
            name="Titan",
            max_health=120,
            engine=Engine(65),
            turbo=TurboCharger(cost=3, boost=15),
            attack=40,
            resistance=20,
            repair_amount=15,
            repair_quota=3,
        )

    def ability_name(self):
        return "Armor"

    def modify_incoming_damage(self, raw):
        return (raw + 1) // 2