import argparse
import itertools
from advent_helpers import run_intcode, get_permutations_of_list


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

    part_1_best_order, part_1_best_power = find_best_power(program_ints, [0, 1, 2, 3, 4], debug)
    print(f"Part 1:\n{part_1_best_order}: {part_1_best_power}\n")

    part_2_best_order, part_2_best_power = find_best_power_rec(program_ints, [5, 6, 7, 8, 9], debug)
    print(f"Part 2:\n{part_2_best_order}: {part_2_best_power}")


def find_best_power(program_ints, phases, debug):
    best_power = 0
    best_order = []
    for inputs in get_permutations_of_list(phases):
        power = 0
        for phase in inputs:
            program_outputs = [x for x in run_intcode(program_ints, (p for p in [phase, power]), debug)]
            if len(program_outputs) != 1:
                raise Exception(f"Should be 1 output but found {len(program_outputs)}")
            power = program_outputs[0]
        if power > best_power:
            best_power = power
            best_order = inputs
        if debug:
            print(f"{inputs}: {power}")
    return best_order, best_power


def find_best_power_rec(program_ints, phases, debug):
    best_power = 0
    best_order = []
    for phase_order in get_permutations_of_list(phases):
        last_output = 0

        def input_generator(i):
            yield i
            while True:
                yield last_output

        for program in itertools.cycle([run_intcode(program_ints, input_generator(i), debug) for i in phase_order]):
            new_output = next(program, None)
            if new_output is None:
                break
            else:
                last_output = new_output
        if last_output > best_power:
            best_power = last_output
            best_order = phase_order
        if debug:
            print(f"{phase_order}: {last_output}")
    return best_order, best_power


if __name__ == "__main__":
    main()
