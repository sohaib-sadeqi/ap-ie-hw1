from abc import ABC, abstractmethod

from .engine import Engine
from .tire import SlickTire, make_tire
from .turbo import TurboCharger


class Car(ABC):
    def __init__(self, name, max_health, engine, turbo, attack,
                 resistance, repair_amount, repair_quota):
        if not name:
            raise ValueError("car name cannot be empty")
        if max_health <= 0:
            raise ValueError("max_health must be positive")
        if repair_amount < 0 or repair_quota < 0:
            raise ValueError("repair amount and quota cannot be negative")
        if not isinstance(engine, Engine):
            raise TypeError("engine must be an Engine")
        if not isinstance(turbo, TurboCharger):
            raise TypeError("turbo must be a TurboCharger")

        self._name = name
        self._max_health = max_health
        self._health = max_health
        self._engine = engine
        self._turbo = turbo
        self._attack = attack
        self._resistance = resistance
        self._repair_amount = repair_amount
        self._remaining_repairs = repair_quota
        self._distance = 0
        self._active = True
        self._tire = SlickTire()

    @abstractmethod
    def ability_name(self):
        # Return a readable name for this car's special ability.
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @property
    def max_health(self):
        return self._max_health

    @property
    def distance(self):
        return self._distance

    @property
    def attack(self):
        return self._attack

    @property
    def resistance(self):
        return self._resistance

    @property
    def tire(self):
        return self._tire

    @property
    def turbo(self):
        return self._turbo

    @property
    def remaining_repairs(self):
        return self._remaining_repairs

    @property
    def is_active(self):
        return self._active

    def is_turbo_on(self):
        return self._turbo.is_on

    def modify_move_base(self, base):
        return base

    def modify_incoming_damage(self, raw):
        return raw

    def move(self, weather):
        if not self._active:
            return 0

        base = self._engine.base_output(self._health, self._max_health)
        base = self.modify_move_base(base)
        # effective_factor reads tire durability before wear.
        factor = self._tire.effective_factor(weather)
        drive = (base * factor) // 100
        gain = drive + self._turbo.consume()

        self._distance += gain
        self._tire.wear()
        return gain

    def activate_turbo(self):
        if not self._active or self._turbo.is_on:
            return False

        cost = self._turbo.activation_cost()
        self._turbo.activate()
        self._health -= cost
        if self._health <= 0:
            self._health = 0
            self._eliminate()
        return True

    def receive_damage(self, raw):
        damage = self.modify_incoming_damage(raw)
        if damage <= 0:
            return False

        old_health = self._health
        self._health = max(0, self._health - damage)
        if self._health == 0:
            self._eliminate()
        return self._health != old_health

    def repair(self):
        if (not self._active or self._remaining_repairs == 0
                or self._health == self._max_health):
            return False

        self._health = min(self._max_health, self._health + self._repair_amount)
        self._remaining_repairs -= 1
        self._turbo.reset()
        return True

    def pit(self, tire_code):
        if not self._active or self._health <= 5:
            return False

        # Validate/build first so an invalid code cannot partially change state.
        new_tire = make_tire(tire_code)
        self._health -= 5
        self._tire = new_tire
        self._turbo.reset()
        return True

    def snapshot(self):
        return {
            "health": self._health,
            "distance": self._distance,
            "active": self._active,
            "repairs": self._remaining_repairs,
            "tire": self._tire.snapshot(),
            "turbo": self._turbo.snapshot(),
        }

    def restore(self, state):
        tire_state = state["tire"]
        restored_tire = make_tire(tire_state["code"])
        restored_tire.restore_from(tire_state)

        self._health = state["health"]
        self._distance = state["distance"]
        self._active = state["active"]
        self._remaining_repairs = state["repairs"]
        self._tire = restored_tire
        self._turbo.restore_from(state["turbo"])

    def _eliminate(self):
        self._health = 0
        self._active = False
        self._turbo.reset()
