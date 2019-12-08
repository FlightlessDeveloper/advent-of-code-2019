import argparse


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

    best_power = 0
    best_order = []
    for inputs in get_permutations_of_list([0, 1, 2, 3, 4]):
        power = 0
        for phase in inputs:
            program_outputs = run_program(program_ints, [phase, power], debug)
            if len(program_outputs) != 1:
                raise Exception(f"Should be 1 output but found {len(program_outputs)}")
            power = program_outputs[0]
        if power > best_power:
            best_power = power
            best_order = inputs
        print(f"{inputs}: {power}")
    print(f"Best order is {best_order} with a power of {best_power}")


def get_permutations_of_list(l):
    if (len(l)) == 0:
        return [[]]
    else:
        return [[l[i]] + tail for i in range(len(l)) for tail in get_permutations_of_list(l[:i] + l[i + 1:])]


# This is copied from day 05 with minor alterations
def run_program(program_ints, input_values, debug=False):
    tape = [x for x in program_ints]
    head = 0
    inputs_head = 0
    # We need to read the output values rather than print them this time
    output_values = []
    while head < len(tape):
        if debug:
            debug_print_tape(tape, head)
        intcode = tape[head]
        opcode = intcode % 100
        if opcode == 1:
            # Add
            lhs, rhs, out = calculate_args(intcode, tape, head, 3)
            if debug:
                print(f"01 add {arg_to_string(tape, lhs)}, {arg_to_string(tape, rhs)}, {arg_to_string(tape, out)}")
            write_at_parameter(tape, out, read_at_parameter(tape, lhs) + read_at_parameter(tape, rhs))
            head += 4
        elif opcode == 2:
            # Multiply
            lhs, rhs, out = calculate_args(intcode, tape, head, 3)
            if debug:
                print(f"02 multiply {arg_to_string(tape, lhs)}, {arg_to_string(tape, rhs)}, {arg_to_string(tape, out)}")
            write_at_parameter(tape, out, read_at_parameter(tape, lhs) * read_at_parameter(tape, rhs))
            head += 4
        elif opcode == 3:
            # Input
            arg, = calculate_args(intcode, tape, head, 1)
            if debug:
                print(f"03 input {arg_to_string(tape, arg)}, {input_values[inputs_head]}")
            write_at_parameter(tape, arg, input_values[inputs_head])
            inputs_head += 1
            head += 2
        elif opcode == 4:
            # Output
            arg, = calculate_args(intcode, tape, head, 1)
            if debug:
                print(f"04 output {arg_to_string(tape, arg)}")
            output = read_at_parameter(tape, arg)
            output_values += [output]
            head += 2
        elif opcode == 5:
            # Jump if true
            cond, new_head = calculate_args(intcode, tape, head, 2)
            if debug:
                print(f"05 jump-if-true {arg_to_string(tape, cond)}, {arg_to_string(tape, new_head)}")
            if read_at_parameter(tape, cond) != 0:
                head = read_at_parameter(tape, new_head)
            else:
                head += 3
        elif opcode == 6:
            # Jump if false
            cond, new_head = calculate_args(intcode, tape, head, 2)
            if debug:
                print(f"06 jump-if-false {arg_to_string(tape, cond)}, {arg_to_string(tape, new_head)}")
            if read_at_parameter(tape, cond) == 0:
                head = read_at_parameter(tape, new_head)
            else:
                head += 3
        elif opcode == 7:
            # Less than
            lhs, rhs, out = calculate_args(intcode, tape, head, 3)
            if debug:
                print(f"07 less-than {arg_to_string(tape, lhs)}, {arg_to_string(tape, rhs)}, {arg_to_string(tape, out)}")
            result = 1 if read_at_parameter(tape, lhs) < read_at_parameter(tape, rhs) else 0
            write_at_parameter(tape, out, result)
            head += 4
        elif opcode == 8:
            # Equals
            lhs, rhs, out = calculate_args(intcode, tape, head, 3)
            if debug:
                print(f"08 equals {arg_to_string(tape, lhs)}, {arg_to_string(tape, rhs)}, {arg_to_string(tape, out)}")
            result = 1 if read_at_parameter(tape, lhs) == read_at_parameter(tape, rhs) else 0
            write_at_parameter(tape, out, result)
            head += 4
        elif opcode == 99:
            if debug:
                print(f"99 STOP")
            break
        else:
            raise Exception(f"Unknown opcode '{opcode}'")
    return output_values


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
        return f"pos:{value}({tape[value]})"
    elif mode == 1:
        return f"imm:{value}"
    else:
        return f"invalid({mode}){value}"


if __name__ == "__main__":
    main()
