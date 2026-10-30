"""Replaceable race-finish policies for sprint and time-attack modes."""

from abc import ABC, abstractmethod

from .ranking import best_active


class RaceRule(ABC):
    """Common contract used by Race to check intermediate and final results."""

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
        """Return an immediate result after a move, or None to keep racing."""
        raise NotImplementedError

    def final_result(self, cars):
        """Return the distance-based final result shared by both modes."""
        winner = best_active(cars)
        if winner is None:
            return "NO WINNER"
        return f"WINNER {winner.name} DISTANCE"


class SprintRule(RaceRule):
    """Finish immediately when a car's move reaches the finish distance."""

    MODE = "SPRINT"

    def after_move(self, car):
        if car.is_active and car.distance >= self.finish_distance:
            return f"WINNER {car.name} FINISH"
        return None


class TimeAttackRule(RaceRule):
    """Always process all commands; choose the ranked car at the end."""

    MODE = "TIME_ATTACK"

    def after_move(self, car):
        # Crossing the finish line has no immediate effect in this mode.
        return None


def make_rule(mode, finish_distance):
    """Create the selected policy from the input mode token."""
    if mode == SprintRule.MODE:
        return SprintRule(finish_distance)
    if mode == TimeAttackRule.MODE:
        return TimeAttackRule(finish_distance)
    raise ValueError(f"unknown race mode: {mode}")
