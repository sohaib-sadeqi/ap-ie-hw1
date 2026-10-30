from .base import Command
from race import ranking
from domain.state import CarSnapshot

class MoveCommand(Command):
    def __init__(self, company):
        self.company = company
        
    def execute(self, race):
        car = race.get_car(self.company)

        def move_and_check_finish():
            car.move(race.weather.state)
            return race.after_move(car)

        return race.run_mutation(move_and_check_finish)

class TurboCommand(Command):
    def __init__(self, company):
        self.company = company

    def execute(self, race):
        car = race.get_car(self.company)
        return race.run_mutation(car.activate_turbo)


class CollisionCommand(Command):
    def __init__(self, attacker, target):
        self.attacker = attacker
        self.target = target

    def execute(self, race):
        attacker_car = race.get_car(self.attacker)
        target_car = race.get_car(self.target)

        def apply_collision():
            if not attacker_car.is_active or not target_car.is_active:
                return False
            raw = max(0, attacker_car.attack - target_car.resistance)
            return target_car.receive_damage(raw)

        return race.run_mutation(apply_collision)

class RepairCommand(Command):
    def __init__(self, company):
        self.company = company

    def execute(self, race):
        car = race.get_car(self.company)
        return race.run_mutation(car.repair)

class WeatherCommand(Command):
    def __init__(self, weather):
        self.weather = weather
        
    def execute(self, race):
        return race.run_mutation(lambda: race.change_weather(self.weather))

class PitCommand(Command):
    def __init__(self, company, tire):
        self.company = company
        self.tire = tire

    def execute(self, race):
        car = race.get_car(self.company)
        return race.run_mutation(lambda: car.pit(self.tire))

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
        return race.undo()

