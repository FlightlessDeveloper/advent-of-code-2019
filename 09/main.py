import argparse
from advent_helpers import run_intcode


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("program_inputs", nargs='*')
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    input_lines = [x for x in open(args.input_file)]
    # Assume input is all on the first line
    program_ints = [int(x) for x in input_lines[0].split(",")]
    program_inputs = [int(x) for x in args.program_inputs]

    output = run_intcode(program_ints, (x for x in program_inputs), args.debug)
    print(f"Output: {[x for x in output]}")


if __name__ == "__main__":
    main()
