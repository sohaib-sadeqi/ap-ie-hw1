

class Race:
    def __init__(self, weather, cars, rule):
        self.weather = weather # Object from Weather
        self.rule = rule # object from RaceRule (one of TimeAttachRule or SprintRule)
        self._cars = cars
        self._finished = False
        self._result = None

    def get_car(self, name):
        for c in self._cars.values():
            if c.name == name: 
                return c
        return None

    def iter_cars(self):
        return [car for car in self._cars if car.is_active]

    def change_weather(self, state):
        return self.weather.change_to(state)

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
        self.rule.final_result(self._cars)
