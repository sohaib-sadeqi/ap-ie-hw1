from .base import Command
from race import ranking
from domain.state import CarSnapshot

class MoveCommand(Command):
    def __init__(self, company):
        self.company = company
        
    def execute(self, race):
        car = race.get_car(self.company)
        car.move(race.weather.state)
        return race.after_move(car)

class TurboCommand(Command):
    def __init__(self, company):
        self.company = company

    def execute(self, race):
        car = race.get_car(self.company)
        return car.activate_turbo()


class CollisionCommand(Command):
    def __init__(self, attacker, target):
        self.attacker = attacker
        self.target = target

    def execute(self, race):
        attackerCar = race.get_car(self.attacker)
        targetCar = race.get_car(self.target)
        if not attackerCar.is_active or not targetCar.is_active:
            return False
        
        raw = max(0, attackerCar.attack - targetCar.resistance)
        return targetCar.receive_damage(raw)

class RepairCommand(Command):
    def __init__(self, company):
        self.company = company

    def execute(self, race):
        car = race.get_car(self.company)
        return car.repair()

class WeatherCommand(Command):
    def __init__(self, weather):
        self.weather = weather
        
    def execute(self, race):
        return race.change_weather(self.weather)

class PitCommand(Command):
    def __init__(self, company, tire):
        self.company = company
        self.tire = tire

    def execute(self, race):
        car = race.get_car(self.company)
        return car.pit(self.tire)

class StatusCommand(Command):
    def __init__(self, company):
        self.company = company

    def execute(self, race):
        car = race.get_car(self.company)

        turbo_boost = (
            car.turbo.pending_boost
            if car.is_turbo_on()
            else None
        )

        snapshot = CarSnapshot(
            name=car.name,
            is_active=car.is_active,
            health=car.health,
            distance=car.distance,
            turbo_boost=turbo_boost,
            tire_name=car.tire.code(),
            durability=car.tire.durability,
            repairs_left=car.remaining_repairs,
        )

        return snapshot.status_line()

class RankCommand(Command):
    def __init__(self):
        pass

    def execute(self, race):
        return ranking.format_rank(race.iter_cars())

class UndoCommand(Command):
    def __init__(self):
        pass

    def execute(self, race):
        return False

