import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    paths_local = [parse_wire(wire) for wire in open(args.input_file)]
    traced_wires = [trace_wire(wire) for wire in paths_local]

    crossover_points = set(traced_wires[0].keys()).intersection(set(traced_wires[1].keys()))
    print(f"Sorted by distance:\n{sorted(crossover_points, key=lambda p: manhatten_distance((0, 0), p))}\n")
    crossovers_with_steps = [(x, y, traced_wires[0][x, y] + traced_wires[1][x, y]) for (x, y) in crossover_points]
    print(f"Sorted by total steps:\n{sorted(crossovers_with_steps, key=lambda x: x[2])}")


def parse_wire(wire_string):
    return [(int(s[1:]), s[0]) for s in wire_string.split(",")]


def trace_wire(wire_local):
    x, y, steps = 0, 0, 0
    steps_per_location = dict()

    for (length, direction) in wire_local:
        if direction == "L":
            for cx in range(x, x - length, -1):
                if (cx, y) not in steps_per_location:
                    steps_per_location[(cx, y)] = steps
                steps += 1
            x -= length
        elif direction == "R":
            for cx in range(x, x + length):
                if (cx, y) not in steps_per_location:
                    steps_per_location[(cx, y)] = steps
                steps += 1
            x += length
        elif direction == "D":
            for cy in range(y, y - length, -1):
                if (x, cy) not in steps_per_location:
                    steps_per_location[(x, cy)] = steps
                steps += 1
            y -= length
        elif direction == "U":
            for cy in range(y, y + length):
                if (x, cy) not in steps_per_location:
                    steps_per_location[(x, cy)] = steps
                steps += 1
            y += length
        else:
            raise Exception(f"Invalid direction '{direction}'")
    return steps_per_location


def manhatten_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == "__main__":
    main()
