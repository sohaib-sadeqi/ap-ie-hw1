class Weather:
    DRY = "DRY"
    WET = "WET"
    VALID_STATES = frozenset((DRY, WET))

    def __init__(self, state=DRY):
        self._state = state
        self._validate(state)

    @property
    def state(self):
        return self._state

    def change_to(self, state):
        self._validate(state)
        if state == self._state:
            return False
        self._state = state
        return True

    def snapshot(self):
        return self._state

    def restore(self, state):
        self._validate(state)
        self._state = state

    @classmethod
    def _validate(cls, state):
        if state not in cls.VALID_STATES:
            raise ValueError(f"unknown weather state: {state}")
