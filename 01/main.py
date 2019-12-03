import argparse
import math


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    module_masses = [int(x) for x in open(args.input_file)]

    initial_fuel_required = sum(mass_to_fuel(x) for x in module_masses)
    print(f"Initial fuel required: {initial_fuel_required}")

    total_fuel_required = sum(mass_to_fuel_including_fuel(x) for x in module_masses)
    print(f"Total fuel required: {total_fuel_required}")


def mass_to_fuel(mass):
    return math.floor(mass / 3) - 2


def mass_to_fuel_including_fuel(mass):
    new_mass = mass_to_fuel(mass)
    if new_mass > 0:
        return new_mass + mass_to_fuel_including_fuel(new_mass)
    else:
        return 0


if __name__ == "__main__":
    main()
