"""Track conditions (the weather) and the Track object that remembers the current one."""
class Weather:
    DRY = "DRY"
    WET = "WET"

    def __init__(self):
        self._state = Weather.DRY

    @property
    def state(self):
        return self._state

    def change_to(self, state):
        if state == self._state:
            return False
        self._state = state
        return True