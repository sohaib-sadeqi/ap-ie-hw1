from copy import deepcopy


class RaceSnapshot:
    def __init__(self, weather_state: str, cars_state: dict[str, dict]):
        self.weather_state = weather_state
        self.cars_state = cars_state

    @classmethod
    def capture(cls, weather, cars) -> "RaceSnapshot":
        return cls(weather.state, {n: c._state_dict() for n, c in cars.items()})