import argparse


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

    final_tape = run_program(program_ints, program_inputs, args.debug)
    print(f"Final tape: {final_tape}")


def run_program(program_ints, input_values, debug=False):
    tape = [x for x in program_ints]
    head = 0
    inputs_head = 0
    while head < len(tape):
        if debug:
            debug_print_tape(tape, head)
        intcode = tape[head]
        opcode = intcode % 100
        if opcode == 1:
            # Add
            lhs, rhs, out = calculate_args(intcode, tape, head, 3)
            if debug:
                print(f"add {arg_to_string(tape, lhs)}, {arg_to_string(tape, rhs)}, {arg_to_string(tape, out)}")
            write_at_parameter(tape, out, read_at_parameter(tape, lhs) + read_at_parameter(tape, rhs))
            head += 4
        elif opcode == 2:
            # Multiply
            lhs, rhs, out = calculate_args(intcode, tape, head, 3)
            if debug:
                print(f"multiply {arg_to_string(tape, lhs)}, {arg_to_string(tape, rhs)}, {arg_to_string(tape, out)}")
            write_at_parameter(tape, out, read_at_parameter(tape, lhs) * read_at_parameter(tape, rhs))
            head += 4
        elif opcode == 3:
            # Input
            arg, = calculate_args(intcode, tape, head, 1)
            if debug:
                print(f"input {arg_to_string(tape, arg)}, {input_values[inputs_head]}")
            write_at_parameter(tape, arg, input_values[inputs_head])
            inputs_head += 1
            head += 2
        elif opcode == 4:
            # Output
            arg, = calculate_args(intcode, tape, head, 1)
            if debug:
                print(f"output {arg_to_string(tape, arg)}")
            output = read_at_parameter(tape, arg)
            print(f"Message from program: '{output}'")
            head += 2
        elif opcode == 99:
            # Stop
            break
        else:
            raise Exception(f"Unknown opcode '{opcode}'")
    return tape


def calculate_args(intcode, tape, head, num_args):
    return [((intcode // (10 ** (arg_num + 2))) % 10, tape[head + arg_num + 1]) for arg_num in range(num_args)]


def read_at_parameter(tape, param):
    mode, value = param
    if mode == 0:
        # Position
        return tape[value]
    elif mode == 1:
        # Immediate
        return value
    else:
        raise Exception(f"Invalid parameter mode '{mode}'")


def write_at_parameter(tape, param, new_value):
    mode, value = param
    if mode == 0:
        # Position
        tape[value] = new_value
    elif mode == 1:
        # Immediate
        raise Exception(f"Can't write to immediate parameter '{mode}'")
    else:
        raise Exception(f"Invalid parameter mode '{mode}'")


def debug_print_tape(tape, head):
    print(", ".join(
        [(f"___{i}:{str(tape[i])}___" if i == head else f"{i}:{str(tape[i])}")
         for i in range(len(tape))]
    ) + "\n")


def arg_to_string(tape, arg):
    mode, value = arg
    if mode == 0:
        return f"pos:[{value}]->{tape[value]}"
    elif mode == 1:
        return f"imm:{value}"
    else:
        return f"invalid({mode}){value}"


if __name__ == "__main__":
    main()
