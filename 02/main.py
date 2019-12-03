import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    input_lines = [x for x in open(args.input_file)]
    # Assume input is all on the first line
    initial_program = [int(x) for x in input_lines[0].split(",")]

    memory = [x for x in initial_program]
    memory[1] = 12
    memory[2] = 2
    for index in range(0, len(memory), 4):
        instruction = memory[index]
        left_pos = memory[index + 1]
        right_pos = memory[index + 2]
        out_pos = memory[index + 3]

        if instruction == 1:
            memory[out_pos] = memory[left_pos] + memory[right_pos]
        elif instruction == 2:
            memory[out_pos] = memory[left_pos] * memory[right_pos]
        elif instruction == 99:
            break
        else:
            raise Exception(f"Invalid instruction code '{instruction}'")
    print(f"Final memory: {memory}")


if __name__ == "__main__":
    main()
