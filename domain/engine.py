
class engine:
    def __init__(self, power: int):
        self._power = power
   
    @property
    def power(self):
        return self._power
    
    def base_output(self, health, max_health):
        return (self._power * health) // max_health