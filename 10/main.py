import argparse
from collections import defaultdict
from math import atan, pi


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("goal_destroyed", default=0)
    return parser.parse_args()


def main():
    args = parse_args()
    meteor_map = [[c for c in x.strip()] for x in open(args.input_file) if len(x.strip()) > 0]
    part_2_goal_index = int(args.goal_destroyed) - 1

    (x, y), score = find_best_meteor_pos(meteor_map)
    print(f"Best meteor at ({x}, {y}) can see {score} other meteors")

    part_2_x, part_2_y, _, _ = get_destroyed_meteors(x, y, meteor_map)[part_2_goal_index]
    print(f"{part_2_goal_index + 1}th destroyed meteor: ({part_2_x}, {part_2_y})")


def find_best_meteor_pos(meteor_map):
    best_meteor_score = 0
    best_meteor_pos = (0, 0)
    for y in range(len(meteor_map)):
        for x in range(len(meteor_map[y])):
            if meteor_map[y][x] == '#':
                score = len(get_visible_meteors(x, y, meteor_map))
                if score > best_meteor_score:
                    best_meteor_score = score
                    best_meteor_pos = (x, y)
    return best_meteor_pos, best_meteor_score


def get_visible_meteors(x, y, meteor_map):
    angles_to_meteors = defaultdict(lambda: [])
    for target_y in range(len(meteor_map)):
        for target_x in range(len(meteor_map[target_y])):
            if meteor_map[target_y][target_x] == '#' and not (x == target_x and y == target_y):
                x_diff = abs(x - target_x)
                y_diff = abs(y - target_y)
                if x_diff == 0:
                    if target_y < y:
                        angle = 0
                    else:
                        angle = pi
                elif y_diff == 0:
                    if target_x > x:
                        angle = pi / 2
                    else:
                        angle = 3 * pi / 2
                elif target_x > x and target_y < y:
                    angle = atan(x_diff / y_diff)
                elif target_x > x and target_y > y:
                    angle = (pi / 2) + atan(y_diff / x_diff)
                elif target_x < x and target_y > y:
                    angle = pi + atan(x_diff / y_diff)
                elif target_x < x and target_y < y:
                    angle = (3 * pi / 2) + atan(y_diff / x_diff)
                angles_to_meteors[angle].append((target_x, target_y, angle, x_diff))
    return [sorted(angles_to_meteors[key], key=lambda angle: angle[3])[0] for key in angles_to_meteors.keys()]


def get_destroyed_meteors(x, y, meteor_map):
    altered_map = [x for x in meteor_map]
    destroyed_meteors = []
    while True:
        visible_meteors = sorted(get_visible_meteors(x, y, altered_map), key=lambda m: m[2])
        if len(visible_meteors) == 0:
            break
        destroyed_meteors.extend(visible_meteors)
        for x, y, _, _ in visible_meteors:
            altered_map[y][x] = '.'
    return destroyed_meteors


if __name__ == "__main__":
    main()
