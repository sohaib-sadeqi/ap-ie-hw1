"""The engine: turns health into base power."""
class Engine:
    def __init__(self, power):
        self._power = power

    def base_power(self, health, max_health):
        # The more damaged the car, the weaker the engine.
        return (self._power * health) // max_health
