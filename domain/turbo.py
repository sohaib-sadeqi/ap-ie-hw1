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

    def snapshot(self):
        return {"pending": self._pending}

    def restore_from(self, state):
        pending = state["pending"]
        if pending < 0:
            raise ValueError("pending boost cannot be negative")
        self._pending = pending


class OverboostTurbo(TurboCharger):
    def __init__(self):
        super().__init__(cost=10, boost=50)
        self._used = False

    @property
    def used(self):
        return self._used

    def activation_cost(self):
        return 10 if self._used else 20

    def activate(self):
        self._pending = 50 if self._used else 75
        self._used = True

    def snapshot(self):
        state = super().snapshot()
        state["used"] = self._used
        return state

    def restore_from(self, state):
        super().restore_from(state)
        self._used = state["used"]
