from abc import ABC, abstractmethod
from .ranking import best_active


class RaceRule(ABC):
    MODE = None

    def __init__(self, finish_distance):
        if finish_distance <= 0:
            raise ValueError("finish distance must be positive")
        self._finish_distance = finish_distance

    @property
    def finish_distance(self):
        return self._finish_distance

    @property
    def mode(self):
        return self.MODE

    @abstractmethod
    def after_move(self, car):
        raise NotImplementedError

    def final_result(self, cars):
        winner = best_active(cars)
        if winner is None:
            return "NO WINNER"
        return f"WINNER {winner.name} DISTANCE"


class SprintRule(RaceRule):
    MODE = "SPRINT"

    def after_move(self, car):
        if car.is_active and car.distance >= self.finish_distance:
            return f"WINNER {car.name} FINISH"
        return None


class TimeAttackRule(RaceRule):
    MODE = "TIME_ATTACK"

    def after_move(self, car):
        # Crossing the finish line has no immediate effect in this mode.
        return None


def make_rule(mode, finish_distance):
    if mode == SprintRule.MODE:
        return SprintRule(finish_distance)
    if mode == TimeAttackRule.MODE:
        return TimeAttackRule(finish_distance)
    raise ValueError(f"unknown race mode: {mode}")
