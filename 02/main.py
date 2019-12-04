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

    for verb in range(0, 100):
        for noun in range(0, 100):
            memory = [x for x in initial_program]
            memory[1] = noun
            memory[2] = verb
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
            out = memory[0]
            if (noun == 12 and verb == 2) or out == 19690720:
                print(f"The output for {noun}, {verb} is {out}")


if __name__ == "__main__":
    main()
