import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    orbit_map = dict((x[4:7], x[0:3]) for x in open(args.input_file) if len(x) > 0)

    print(f"Number of direct and indirect orbits: {sum(get_num_orbits(orbit_map, planet) for planet in orbit_map.keys())}\n")

    you_path = get_path_to_orbit(orbit_map, "YOU")
    santa_path = get_path_to_orbit(orbit_map, "SAN")
    common_path = [x for x in you_path if x in santa_path]

    print(f"Your path: {'('.join(you_path)}\n")
    print(f"Santa's path: {'('.join(santa_path)}\n")
    print(f"Common path: {'('.join(common_path)}\n")

    distance = len(get_path_to_orbit(orbit_map, "YOU", common_path[0])) + len(get_path_to_orbit(orbit_map, "SAN", common_path[0]))
    print(f"Distance to santa: {distance}\n")


def get_num_orbits(orbit_map, planet, end="COM"):
    if planet == end:
        return 0
    else:
        return 1 + get_num_orbits(orbit_map, orbit_map[planet])


def get_path_to_orbit(orbit_map, planet, end="COM"):
    next_planet = orbit_map[planet]
    path = []
    while next_planet != end:
        next_planet = orbit_map[next_planet]
        path.append(next_planet)
    return path


if __name__ == "__main__":
    main()
