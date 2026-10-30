class Engine:
    def __init__(self, power):
        if power < 0:
            raise ValueError("engine power cannot be negative")
        self._power = power

    @property
    def power(self):
        return self._power

    def base_output(self, health, max_health):
        if max_health <= 0:
            raise ValueError("max_health must be positive")
        health = max(0, min(health, max_health))
        return (self._power * health) // max_health

    # Keep the original name available while the rest of the project migrates.
    def base_power(self, health, max_health):
        return self.base_output(health, max_health)
