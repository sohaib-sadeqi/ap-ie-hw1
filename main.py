import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from commands.parser import parse_command
from domain.cars import BlazeCar, TitanCar, VelocityCar
from domain.weather import Weather
from race.race import Race
from race.rules import make_rule

# The project file is named io.py, which collides with Python's standard
# library module named io. Load this sibling file by path to avoid that clash.
_io_spec = spec_from_file_location(
    "hw1_project_io", Path(__file__).with_name("io.py")
)
_project_io = module_from_spec(_io_spec)
_io_spec.loader.exec_module(_project_io)
read_input = _project_io.read_input
write_output = _project_io.write_output


def main():
    input_stream = sys.stdin
    output_stream = sys.stdout

    finish_distance, _command_count, mode, command_lines = read_input(
        input_stream.read()
    )

    cars = {
        "Velocity": VelocityCar(),
        "Blaze": BlazeCar(),
        "Titan": TitanCar(),
    }
    weather = Weather()
    rule = make_rule(mode, finish_distance)
    race = Race(weather, cars, rule)

    output_lines = []
    for line in command_lines:
        command = parse_command(line)
        result = command.execute(race)
        if result is not None:
            output_lines.append(result)
        if race.is_finished:
            break

    # SPRINT sets race.is_finished on an immediate finish. Otherwise both
    # policies choose the distance-based winner after all commands are handled.
    if not race.is_finished:
        output_lines.append(rule.final_result(cars))

    write_output(output_lines, output_stream)


if __name__ == "__main__":
    main()
