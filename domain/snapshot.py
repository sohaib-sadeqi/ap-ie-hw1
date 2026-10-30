from copy import deepcopy
from dataclasses import dataclass


@dataclass(frozen=True)
class RaceSnapshot:
    weather_state: str
    cars_state: dict[str, dict]

    @classmethod
    def capture(cls, weather, cars):
        """Copy weather and each car's public snapshot for later restoration."""
        return cls(
            weather_state=weather.snapshot(),
            cars_state={name: deepcopy(car.snapshot()) for name, car in cars.items()},
        )

    def restore(self, weather, cars):
        """Restore the saved weather and each matching car in place."""
        weather.restore(self.weather_state)
        for name, state in self.cars_state.items():
            cars[name].restore(deepcopy(state))
