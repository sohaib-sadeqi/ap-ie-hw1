"""Turbochargers. Each one knows its own cost/boost rules and its own on/off state."""
class TurboCharger:
    def __init__(self, cost, boost):
        self._cost = cost
        self._boost = boost
        self._pending = 0

    @property
    def is_on(self):
        return self._pending > 0

    @property
    def pending_boost(self):
        return self._pending

    def activation_cost(self):
        return self._cost

    def activate(self):
        self._pending = self._boost

    def consume(self):
        boost = self._pending
        self._pending = 0
        return boost

    def reset(self):
        self._pending = 0


class OverboostTurbo(TurboCharger):
    """Blaze's turbo: the first activation is stronger and more expensive."""
    def __init__(self):
        super().__init__(cost=10, boost=50)
        self._used = False

    def activation_cost(self):
        return 10 if self._used else 20

    def activate(self):
        self._pending = 50 if self._used else 75
        self._used = True