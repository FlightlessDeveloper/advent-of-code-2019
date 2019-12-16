import argparse
from copy import copy
from time import sleep
from collections import namedtuple, defaultdict
from advent_helpers import run_intcode


EMPTY_TILE = 0
WALL_TILE = 1
BLOCK_TILE = 2
PADDLE_TILE = 3
BALL_TILE = 4
TILE_TYPE_TO_STRING = {EMPTY_TILE: ' ', WALL_TILE: '█', BLOCK_TILE: '#', PADDLE_TILE: '-', BALL_TILE: 'O'}
Tile = namedtuple("Tile", "position tile_type")
Position = namedtuple("Position", "x, y")
SCORE_POSITION = Position(-1, 0)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--commands", "-c")
    parser.add_argument("--delay", "-d", default=None)
    parser.add_argument("--ai", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    input_lines = [x for x in open(args.input_file)]
    # Assume input is all on the first line
    program_ints = [int(x) for x in input_lines[0].split(",")]
    commands = [c for c in [line for line in open(args.commands)][0]] if args.commands is not None else []
    delay = int(args.delay) if args.delay is not None else None
    ai_mode = args.ai
    quiet = args.quiet

    num_blocks = len(set([t.position for t in get_tile_details(run_intcode(program_ints, iter(()), False))
                         if t.tile_type == BLOCK_TILE]))
    print(f"Number of blocks: {num_blocks}")
    run_game(insert_quarters(program_ints, 2), commands, delay, ai_mode, quiet)


def get_tile_details(it):
    while True:
        try:
            yield Tile(Position(next(it), next(it)), next(it))
        except StopIteration:
            break


def run_game(program_ints, commands, delay, ai_mode, quiet):
    score = 0
    screen = defaultdict(lambda: EMPTY_TILE)
    ui_iterator = handle_user_interaction(lambda: (screen, score), commands, delay, ai_mode, quiet)
    screen_generator = run_intcode(program_ints, ui_iterator, False)
    for screen_update in get_tile_details(screen_generator):
        if screen_update.position == SCORE_POSITION:
            score = screen_update.tile_type
        else:
            screen[screen_update.position] = screen_update.tile_type
    draw_screen(screen, score, None, quiet)
    print(f"Final Score: {score}")


def insert_quarters(program_ints, quantity):
    funded_program_ints = copy(program_ints)
    funded_program_ints[0] = quantity
    return funded_program_ints


def handle_user_interaction(get_screen, commands, delay, ai_mode, quiet):
    turn = 1
    if ai_mode:
        while True:
            screen, score = get_screen()
            draw_screen(screen, score, turn, quiet)
            ball_location = next(position for position in screen if screen[position] == BALL_TILE)
            paddle_location = next(position for position in screen if screen[position] == PADDLE_TILE)
            if ball_location.x > paddle_location.x:
                yield 1
            elif ball_location.x < paddle_location.x:
                yield -1
            else:
                yield 0
            turn += 1
            sleep(delay / 1000)
    else:
        aborted = False
        last_direction = None
        for c in commands:
            draw_screen(*get_screen(), turn, quiet)
            last_direction = direction_to_input(c, last_direction)
            if last_direction is None:
                aborted = True
                break
            yield last_direction
            turn += 1
            if delay is None:
                input('')
            else:
                print("\n")
                sleep(delay / 1000)
        if not aborted:
            while True:
                draw_screen(*get_screen(), turn, quiet)
                last_direction = direction_to_input(input("> ").lower().strip(), last_direction)
                if last_direction is None:
                    break
                yield last_direction
                turn += 1


def draw_screen(screen, score, turns, quiet):
    if not quiet:
        x_positions = [pos.x for pos in screen if pos != SCORE_POSITION]
        y_positions = [pos.y for pos in screen if pos != SCORE_POSITION]
        print("\n".join("".join(TILE_TYPE_TO_STRING[screen[Position(x, y)]]
                                for x in range(min(x_positions), max(x_positions) + 1))
                        for y in range(min(y_positions), max(y_positions) + 1)))
        if turns is not None:
            print(f"Turn {turns}")
        print(f"Current score: {score}")


def direction_to_input(direction, last_direction):
    if direction == 'a' or direction == 'l':
        return -1
    elif direction == 's' or direction == 'm':
        return 0
    elif direction == 'd' or direction == 'r':
        return 1
    elif direction == 'q':
        return None
    else:
        return last_direction


def will_bounce(tile_type):
    return tile_type == WALL_TILE or tile_type == BLOCK_TILE or tile_type == PADDLE_TILE


if __name__ == "__main__":
    main()
