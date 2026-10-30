from typing import TextIO


def read_input(text):
    lines = text.splitlines()
    if not lines:
        raise ValueError("input is empty")

    header = lines[0].split()
    if len(header) != 3:
        raise ValueError("first line must contain L, N, and MODE")

    finish_distance = int(header[0])
    command_count = int(header[1])
    mode = header[2]
    if command_count < 0:
        raise ValueError("command count cannot be negative")

    command_lines = lines[1:1 + command_count]
    if len(command_lines) != command_count:
        raise ValueError("input contains fewer command lines than N")

    return finish_distance, command_count, mode, command_lines


def write_output(lines, stream: TextIO):
    for line in lines:
        stream.write(f"{line}\n")
