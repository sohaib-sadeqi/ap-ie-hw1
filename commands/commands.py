from .base import Command

class MoveCommand(Command):
    def __init__(self, company):
        self.company = company
        pass

    def execute(self, race):
        car = race.get_car(self.company)
        car.move(race.weather.state)
        return race.after_move(car)

class TurboCommand(Command):

    def execute(self, race):
        pass


class CollisionCommand(Command):

    def execute(self, race):
        pass

class RepairCommand(Command):

    def execute(self, race):
        pass

class WeatherCommand(Command):

    def execute(self, race):
        pass

class PitCommand(Command):

    def execute(self, race):
        pass

class StatusCommand(Command):

    def execute(self, race):
        pass

class RankCommand(Command):

    def execute(self, race):
        pass

class UndoCommand(Command):

    def execute(self, race):
        pass

