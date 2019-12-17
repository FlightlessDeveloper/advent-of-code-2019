import argparse
from copy import copy
from itertools import islice


PHASE_COUNT = 100


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    signal = [int(c) for c in [line.strip() for line in open(args.input_file)][0]]
    debug = args.debug

    phases_it = perform_phases(signal)
    for i in range(PHASE_COUNT + 1):
        phase = next(phases_it)
        if i == PHASE_COUNT or debug:
            print(f"Step {i}: {phase_to_string(phase)}")


def perform_phases(signal):
    last_signal = signal
    yield copy(last_signal)
    while True:
        patterns = [islice(pattern_for_index(i), len(last_signal)) for i in range(len(last_signal))]
        last_signal = [abs(sum(s * p for s, p in zip(last_signal, p_list))) % 10 for p_list in patterns]
        yield copy(last_signal)


def pattern_for_index(i):
    first = True
    while True:
        for x in range(i if first else (i + 1)):
            yield 0
        for x in range(i + 1):
            yield 1
        for x in range(i + 1):
            yield 0
        for x in range(i + 1):
            yield -1
        first = False


def phase_to_string(phase):
    return "".join(str(n) for n in phase)


if __name__ == "__main__":
    main()
