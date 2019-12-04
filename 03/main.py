import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    paths_local = [parse_wire(wire) for wire in open(args.input_file)]
    traced_wires = [trace_wire(wire) for wire in paths_local]

    crossover_points = sorted((point for point in traced_wires[0].intersection(traced_wires[1])), key=lambda p: manhatten_distance((0, 0), p))
    print(f"Crossover points: {crossover_points}")


def parse_wire(wire_string):
    return [(int(s[1:]), s[0]) for s in wire_string.split(",")]


def trace_wire(wire_local):
    x, y = 0, 0
    covered_locations = set()

    for (length, direction) in wire_local:
        if direction == "L":
            new_x = x - length
            covered_locations.update([(cx, y) for cx in range(new_x, x + 1)])
            x = new_x
        elif direction == "R":
            new_x = x + length
            covered_locations.update([(cx, y) for cx in range(x, new_x + 1)])
            x = new_x
        elif direction == "U":
            new_y = y + length
            covered_locations.update([(x, cy) for cy in range(y, new_y + 1)])
            y = new_y
        elif direction == "D":
            new_y = y - length
            covered_locations.update([(x, cy) for cy in range(new_y, y + 1)])
            y = new_y
        else:
            raise Exception(f"Invalid direction '{direction}'")
    return covered_locations


def manhatten_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == "__main__":
    main()
