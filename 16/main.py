import argparse
from copy import copy


PATTERN_SOURCE = [0, 1, 0, -1]
MESSAGE_OFFSET_LENGTH = 7


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    signal = [int(c) for c in [line.strip() for line in open(args.input_file)][0]]
    debug = args.debug

    # Part 1
    perform_steps_loop(signal, 100, debug)

    # Part 2
    get_final_signal(signal, 100, 10000, debug)


def perform_steps_loop(signal, num_steps, debug):
    current_signal = copy(signal)
    for i in range(1, num_steps + 1):
        current_signal = perform_phase(current_signal)
        if i == num_steps or debug:
            print(f"Step {i}: {signal_to_string(current_signal)}")


def perform_phase(signal):
    return [calculate_signal_value(signal, i) for i in range(len(signal))]


def calculate_signal_value(signal, index):
    return abs(sum(pattern_value_for_index(index, i) * signal[i] for i in range(len(signal)))) % 10


def pattern_value_for_index(outer_index, inner_index, starting_offset=1):
    return PATTERN_SOURCE[((inner_index + starting_offset) // (outer_index + 1)) % 4]


def get_final_signal(signal, num_steps, repeat_count, debug):
    answer_first_index = sum(signal[i] * (10 ** (MESSAGE_OFFSET_LENGTH - (i + 1))) for i in range(MESSAGE_OFFSET_LENGTH))
    end_of_signal_reversed = [signal[i % len(signal)]
                              for i in range(len(signal) * repeat_count - 1, answer_first_index - 1, -1)]
    if debug:
        print(f"Step 0: {signal_to_string([x for x in reversed(end_of_signal_reversed)][:8])}")
    for i in range(1, num_steps + 1):
        end_of_signal_reversed = perform_phase_for_final_signal(end_of_signal_reversed)
        if i == num_steps or debug:
            print(f"Step {i}: {signal_to_string([x for x in reversed(end_of_signal_reversed)][:8])}")


def perform_phase_for_final_signal(reversed_signal):
    new_reversed_signal = [0 for _ in reversed_signal]
    new_reversed_signal[0] = reversed_signal[0]
    for i in range(1, len(new_reversed_signal)):
        new_reversed_signal[i] = new_reversed_signal[i - 1] + reversed_signal[i]
    return [abs(x) % 10 for x in new_reversed_signal]


def signal_to_string(phase):
    return "".join(str(n) for n in phase)


if __name__ == "__main__":
    main()
