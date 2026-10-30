from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)  # frozen = nobody can change it after creation
class CarSnapshot:
    name: str
    is_active: bool
    health: int
    distance: int
    turbo_boost: Optional[int]
    tire_name: str
    durability: int
    repairs_left: int

    def status_line(self):
        state = "ACTIVE" if self.is_active else "ELIMINATED"
        turbo = "NONE" if self.turbo_boost is None else str(self.turbo_boost)
        return (f"STATUS {self.name} {state} HP={self.health} DIST={self.distance} "
                f"TURBO={turbo} TIRE={self.tire_name} DUR={self.durability} "
                f"REPAIRS={self.repairs_left}")
