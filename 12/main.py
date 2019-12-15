import argparse
from copy import copy
import operator
from functools import reduce
from itertools import count, takewhile
from collections import namedtuple
from advent_helpers import generate_primes


NUM_STEPS = 1000
Moon = namedtuple("Moon", "position velocity")
Vector3 = namedtuple("Vector3", "x y z")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    moons = [parse_line(x) for x in open(args.input_file) if len(x.strip()) > 0]
    debug = args.debug

    # Part 1
    steps_generator = (x for x in generate_steps(moons, debug))
    if debug:
        print(f"Step 0:\n{moons_to_string(moons)}\n")
    steps = [next(steps_generator) for _ in range(NUM_STEPS + 1)]
    print(f"Energy at step {NUM_STEPS}: {get_energy(steps[NUM_STEPS])}")

    # Part 2
    x_start, x_end = find_repeat(generate_steps([ony_use_axis(moon, 0) for moon in moons], debug))
    print(f"x: {x_start} to {x_end}")
    y_start, y_end = find_repeat(generate_steps([ony_use_axis(moon, 1) for moon in moons], debug))
    print(f"y: {y_start} to {y_end}")
    z_start, z_end = find_repeat(generate_steps([ony_use_axis(moon, 2) for moon in moons], debug))
    print(f"z: {z_start} to {z_end}")
    first_repeat_index = \
        find_lowest_with_factors([x_end - x_start, y_end - y_start, z_end - z_start]) + max(x_start, y_start, z_start)
    print(f"First repeated step is {first_repeat_index}")


def parse_line(s):
    pos = [int(x[2:]) for x in s[1:len(s) - 2].split(", ")]
    return Moon(Vector3(pos[0], pos[1], pos[2]), Vector3(0, 0, 0))


def generate_steps(moon_positions, debug=False):
    moons = [x for x in moon_positions]
    yield copy(moons)
    for step_number in count(1):
        for i, j in [(i, j) for i in range(len(moons)) for j in range(len(moons)) if i < j]:
            moons[i], moons[j] = apply_gravity(moons[i], moons[j])
        for k in range(len(moons)):
            moons[k] = apply_velocity(moons[k])
        if debug:
            print(f"Step {step_number}:\n{moons_to_string(moons)}\n")
        yield copy(moons)


def apply_gravity(l, r):
    x_diff = difference(l.position.x, r.position.x)
    y_diff = difference(l.position.y, r.position.y)
    z_diff = difference(l.position.z, r.position.z)
    new_l_velocity = Vector3(l.velocity.x + x_diff, l.velocity.y + y_diff, l.velocity.z + z_diff)
    new_r_velocity = Vector3(r.velocity.x - x_diff, r.velocity.y - y_diff, r.velocity.z - z_diff)
    return Moon(l.position, new_l_velocity), Moon(r.position, new_r_velocity)


def difference(l, r):
    if l == r:
        return 0
    elif l < r:
        return 1
    else:
        return -1


def apply_velocity(moon):
    new_x = moon.position.x + moon.velocity.x
    new_y = moon.position.y + moon.velocity.y
    new_z = moon.position.z + moon.velocity.z
    return Moon(Vector3(new_x, new_y, new_z), moon.velocity)


def get_energy(moons):
    return sum([(abs(m.position.x) + abs(m.position.y) + abs(m.position.z)) * (abs(m.velocity.x) + abs(m.velocity.y) + abs(m.velocity.z)) for m in moons])


def ony_use_axis(moon, axis):
    return Moon(Vector3(*(v if i == axis else 0 for i, v in enumerate(moon.position))),
                Vector3(*(v if i == axis else 0 for i, v in enumerate(moon.velocity))))


def find_repeat(generator):
    outputs = {}
    for i in count(0):
        next_output = next(generator)
        moons_hash = "".join([hash_moon(m) for m in next_output])
        if moons_hash in outputs:
            return outputs[moons_hash], i
        outputs[moons_hash] = i


def hash_moon(m):
    return f"[{m.position.x}|{m.position.y}|{m.position.z}:{m.velocity.x}|{m.velocity.y}|{m.velocity.z}]"


def find_lowest_with_factors(args):
    prime_factors = set()
    for x in args:
        prime_factors.update(p for p in takewhile(lambda p: p < x, generate_primes()) if x % p == 0)
    step_num = reduce(operator.mul, (x for x in prime_factors), 1)
    for i in count(1):
        test_num = i * step_num
        if all((test_num % x) == 0 for x in args):
            return test_num


def moon_to_string(moon):
    return f"pos=<x={moon.position.x} y={moon.position.y} z={moon.position.z}> " \
           f"vel=<x={moon.velocity.x} y={moon.velocity.y} z={moon.velocity.z}>"


def moons_to_string(moons):
    return "\n".join([moon_to_string(m) for m in moons])


if __name__ == "__main__":
    main()
