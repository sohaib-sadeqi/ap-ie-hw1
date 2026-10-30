"""Convert one textual command into its corresponding Command object."""

from .commands import (
    CollisionCommand,
    MoveCommand,
    PitCommand,
    RankCommand,
    RepairCommand,
    StatusCommand,
    TurboCommand,
    UndoCommand,
    WeatherCommand,
)


def parse_command(line):
    """Parse a command line and return a command object; never execute it."""
    parts = line.split()
    if not parts:
        raise ValueError("command line cannot be empty")

    command_name, *args = parts
    constructors = {
        "MOVE": (MoveCommand, 1),
        "TURBO": (TurboCommand, 1),
        "COLLISION": (CollisionCommand, 2),
        "REPAIR": (RepairCommand, 1),
        "WEATHER": (WeatherCommand, 1),
        "PIT": (PitCommand, 2),
        "STATUS": (StatusCommand, 1),
        "RANK": (RankCommand, 0),
        "UNDO": (UndoCommand, 0),
    }

    if command_name not in constructors:
        raise ValueError(f"unknown command: {command_name}")

    command_class, expected_args = constructors[command_name]
    if len(args) != expected_args:
        raise ValueError(
            f"{command_name} expects {expected_args} argument(s), got {len(args)}"
        )

    return command_class(*args)
