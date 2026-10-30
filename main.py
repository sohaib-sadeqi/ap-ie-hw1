import sys

from commands.parser import parse_command
from domain.cars import BlazeCar, TitanCar, VelocityCar
from domain.weather import Weather
from race.race import Race
from race.rules import make_rule


def main():
    """Read, execute, and report each command as soon as it is available."""
    finish_distance, command_count, mode = sys.stdin.readline().split()
    finish_distance = int(finish_distance)
    command_count = int(command_count)

    cars = {
        "Velocity": VelocityCar(),
        "Blaze": BlazeCar(),
        "Titan": TitanCar(),
    }
    weather = Weather()
    rule = make_rule(mode, finish_distance)
    race = Race(weather, cars, rule)

    for _ in range(command_count):
        line = sys.stdin.readline()
        command = parse_command(line)
        result = command.execute(race)
        if isinstance(result, str):
            print(result, flush=True)

        if race.is_finished:
            break

    if not race.is_finished:
        print(rule.final_result(cars), flush=True)


if __name__ == "__main__":
    main()
