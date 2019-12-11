import argparse
from decimal import Decimal


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    map = [x.strip() for x in open(args.input_file) if len(x.strip()) > 0]

    (x, y), score = find_best_meteor_pos(map)
    print(f"Best meteor at ({x}, {y}) can see {score} other meteors")


def find_best_meteor_pos(map):
    best_meteor_score = 0
    best_meteor_pos = (0, 0)
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                score = count_visible_meteors(x, y, map)
                # print(f"meteor at {x}, {y} can see {score} meteors")
                if score > best_meteor_score:
                    best_meteor_score = score
                    best_meteor_pos = (x, y)
    return best_meteor_pos, best_meteor_score


def count_visible_meteors(x, y, map):
    meteor_angles = set()
    for target_y in range(len(map)):
        for target_x in range(len(map[target_y])):
            if map[target_y][target_x] == '#' and not (x == target_x and y == target_y):
                angle = Decimal(0) if x == target_x or y == target_y else abs(Decimal(x - target_x) / Decimal(y - target_y))
                if x > target_x:
                    h_dir = 'W'
                elif x < target_x:
                    h_dir = 'E'
                else:
                    h_dir = ''
                if y > target_y:
                    v_dir = 'N'
                elif y < target_y:
                    v_dir = 'S'
                else:
                    v_dir = ''
                complete_angle = (v_dir + h_dir, angle)
                meteor_angles.add(complete_angle)
    return len(meteor_angles)


if __name__ == "__main__":
    main()
