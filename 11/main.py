import argparse
from intcomputer import run_intcode


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    input_lines = [x for x in open(args.input_file)]
    # Assume input is all on the first line
    program_ints = [int(x) for x in input_lines[0].split(",")]
    debug = args.debug

    print(f"Panels painted over: {len(paint_panels(program_ints, 0, debug))}")
    print(f"Panel image:\n{panels_to_string(paint_panels(program_ints, 1, debug))}")


def paint_panels(program_ints, starting_panel_int, debug):
    panels = dict()
    panels[(0, 0)] = starting_panel_int
    robot_direction = 'U'
    robot_position = (0, 0)

    def input_generator():
        while True:
            if robot_position in panels:
                yield panels[robot_position]
            else:
                yield 0

    program_output = (x for x in run_intcode(program_ints, input_generator(), debug))

    while True:
        paint_colour_int = next(program_output, None)
        turn_direction_int = next(program_output, None)
        if paint_colour_int is None or turn_direction_int is None:
            break

        if debug:
            print(f"Output: {paint_colour_int}, {turn_direction_int}")
            print(f"Printing {paint_colour_int} at {robot_position}")
        panels[robot_position] = paint_colour_int

        if turn_direction_int == 0:
            # Left
            robot_direction = turn_left(robot_direction)
        elif turn_direction_int == 1:
            # Right
            robot_direction = turn_right(robot_direction)
        else:
            raise Exception(f"Turn direction should be 1 or 0 but was '{turn_direction_int}'")

        robot_position = move_in_direction(robot_position, robot_direction)
        if debug:
            print(f"Robot now at {robot_position} facing {robot_direction}")

    return panels


def panels_to_string(panels):
    xs = [p[0] for p in panels.keys()]
    ys = [p[1] for p in panels.keys()]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    return "\n".join(
        ["".join([get_panel_char(x, y, panels) for x in range(min_x, max_x + 1)]) for y in range(min_y, max_y + 1)])


def get_panel_char(x, y, panels):
    if (x, y) not in panels:
        return ' '
    panel_int = panels[(x, y)]
    if panel_int == 0:
        return ' '
    elif panel_int == 1:
        return '#'
    else:
        raise Exception(f"panel_int should be 1 or 0 but was {panel_int}")


def turn_left(direction):
    if direction == 'U':
        return 'L'
    elif direction == 'L':
        return 'D'
    elif direction == 'D':
        return 'R'
    elif direction == 'R':
        return 'U'
    else:
        raise Exception(f"Robot direction should be was '{direction}'")


def turn_right(direction):
    if direction == 'U':
        return 'R'
    elif direction == 'R':
        return 'D'
    elif direction == 'D':
        return 'L'
    elif direction == 'L':
        return 'U'
    else:
        raise Exception(f"Robot direction should be was '{direction}'")


def move_in_direction(location, direction):
    x, y = location
    if direction == 'U':
        return x, y - 1
    elif direction == 'D':
        return x, y + 1
    elif direction == 'L':
        return x - 1, y
    elif direction == 'R':
        return x + 1, y
    else:
        raise Exception(f"Robot direction should be was '{direction}'")


if __name__ == "__main__":
    main()
