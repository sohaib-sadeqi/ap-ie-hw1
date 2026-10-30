from domain.snapshot import RaceSnapshot


class Race:
    def __init__(self, weather, cars, rule):
        self.weather = weather
        self.rule = rule
        self._cars = cars
        self._finished = False
        self._result = None
        self._history = []

    def get_car(self, name):
        for car in self._cars.values():
            if car.name == name:
                return car
        return None

    def iter_cars(self):
        return [car for car in self._cars.values() if car.is_active]

    def change_weather(self, state):
        return self.weather.change_to(state)

    def run_mutation(self, action):
        before = RaceSnapshot.capture(self.weather, self._cars)
        result = action()
        after = RaceSnapshot.capture(self.weather, self._cars)

        if before != after:
            self._history.append(before)
        return result

    def undo(self):
        if not self._history:
            return False

        snapshot = self._history.pop()
        snapshot.restore(self.weather, self._cars)
        self._finished = False
        self._result = None
        return True

    def after_move(self, car):
        result = self.rule.after_move(car)

        if result is not None:
            self._finished = True
            self._result = result

        return result

    @property
    def is_finished(self):
        return self._finished

    @property
    def result(self):
        return self._result

    def final_result(self):
        return self.rule.final_result(self._cars)
