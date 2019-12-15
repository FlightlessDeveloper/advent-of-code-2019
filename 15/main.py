import argparse
from copy import copy
from collections import defaultdict, namedtuple
from advent_helpers import run_intcode, lambda_to_generator


UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

HIT_WALL = 0
SUCCESS = 1
SUCCESS_FOUND_GOAL = 2

UNKNOWN_TILE = '.'
EMPTY_TILE = ' '
WALL_TILE = '█'
GOAL_TILE = 'X'

Point = namedtuple("Point", "x y")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--steps", "-s", default="10000")
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    input_lines = [x for x in open(args.input_file)]
    # Assume input is all on the first line
    program_ints = [int(x) for x in input_lines[0].split(",")]
    num_steps = int(args.steps)
    debug = args.debug

    final_grid_state = [x for x in discover_maze(program_ints, num_steps, debug)][-1]
    # Solve the maze that this produces to get the answer to part 1
    print(f"\n\nGrid:\n\n{grid_to_string(final_grid_state)}")

    fill_grid_with_oxygen_states = [x for x in fill_grid_with_oxygen(final_grid_state, debug)]
    if debug:
        for i, grid in enumerate(fill_grid_with_oxygen_states):
            print(f"\n\nAfter {i + 1} minutes:\n{grid_to_string(grid)}")
    print(f"\n\nIt takes {len(fill_grid_with_oxygen_states)} minutes to fill with oxygen")


def discover_maze(program_ints, num_steps, debug=False):
    grid = defaultdict(lambda: UNKNOWN_TILE, [(Point(0, 0), EMPTY_TILE)])
    location = Point(0, 0)
    next_input = UP
    program = run_intcode(program_ints, lambda_to_generator(lambda: next_input))

    # First find a wall
    if debug:
        print("Finding a wall")
    while True:
        output = next(program)
        if debug:
            print(f"{next_input} => {output}")
        if output == SUCCESS:
            location = move_point(location, next_input)
            grid[location] = EMPTY_TILE
        elif output == SUCCESS_FOUND_GOAL:
            location = move_point(location, next_input)
            grid[location] = GOAL_TILE
        elif output == HIT_WALL:
            grid[move_point(location, next_input)] = WALL_TILE
            next_input = turn_right(next_input)
            break
        else:
            raise Exception(f"Invalid output: '{output}'")
        yield grid

    # Follow the walls for a bit
    for i in range(num_steps):
        if i != 0 and i % (num_steps // 10) == 0:
            print(f"{(100 * i // num_steps)}%")
        output = next(program)
        if debug:
            print(f"{next_input} => {output}")
        if output == SUCCESS:
            location = move_point(location, next_input)
            grid[location] = EMPTY_TILE
            next_input = turn_left(next_input)
        elif output == SUCCESS_FOUND_GOAL:
            location = move_point(location, next_input)
            grid[location] = GOAL_TILE
            next_input = turn_left(next_input)
        elif output == HIT_WALL:
            grid[move_point(location, next_input)] = WALL_TILE
            next_input = turn_right(next_input)
        else:
            raise Exception(f"Invalid output: '{output}'")
        yield grid


def turn_left(direction):
    if direction == UP:
        return LEFT
    elif direction == LEFT:
        return DOWN
    elif direction == DOWN:
        return RIGHT
    elif direction == RIGHT:
        return UP
    else:
        raise Exception(f"Invalid direction: '{direction}'")


def turn_right(direction):
    if direction == UP:
        return RIGHT
    elif direction == RIGHT:
        return DOWN
    elif direction == DOWN:
        return LEFT
    elif direction == LEFT:
        return UP
    else:
        raise Exception(f"Invalid direction: '{direction}'")


def move_point(point, direction):
    if direction == UP:
        return Point(point.x, point.y - 1)
    elif direction == DOWN:
        return Point(point.x, point.y + 1)
    elif direction == LEFT:
        return Point(point.x - 1, point.y)
    elif direction == RIGHT:
        return Point(point.x + 1, point.y)
    else:
        raise Exception(f"Invalid direction: '{direction}'")


def fill_grid_with_oxygen(grid, debug=False):
    x_points = [point.x for point in grid]
    y_points = [point.y for point in grid]
    min_x = min(x_points)
    max_x = max(x_points) + 1
    min_y = min(y_points)
    max_y = max(y_points) + 1
    oxygenated_grid = copy(grid)
    while count_empty_tiles_in_grid(oxygenated_grid) > 0:
        new_oxygen_points = [point for point in [Point(x, y) for x in range(min_x, max_x) for y in range(min_y, max_y)]
                             if oxygenated_grid[point] == EMPTY_TILE
                             and (oxygenated_grid[Point(point.x - 1, point.y)] == GOAL_TILE
                                  or oxygenated_grid[Point(point.x + 1, point.y)] == GOAL_TILE
                                  or oxygenated_grid[Point(point.x, point.y - 1)] == GOAL_TILE
                                  or oxygenated_grid[Point(point.x, point.y + 1)] == GOAL_TILE)]
        for new_point in new_oxygen_points:
            oxygenated_grid[new_point] = GOAL_TILE
        yield oxygenated_grid


def count_empty_tiles_in_grid(grid):
    return len([None for point in grid if grid[point] == EMPTY_TILE])


def grid_to_string(grid):
    x_positions = [point.x for point in grid]
    y_positions = [point.y for point in grid]
    return "\n".join("".join('O' if x == 0 and y == 0 else grid[Point(x, y)]
                             for x in range(min(x_positions), max(x_positions) + 1))
                     for y in range(min(y_positions), max(y_positions) + 1))


if __name__ == "__main__":
    main()
