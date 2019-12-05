import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("min")
    parser.add_argument("max")
    return parser.parse_args()


def main():
    args = parse_args()
    min = int(args.min)
    max = int(args.max)

    valid_passwords = [n for n in range(min, max + 1) if is_valid_password(str(n))]
    print(f"There are {len(valid_passwords)} valid passwords")

    new_valid_passwords = [n for n in range(min, max + 1) if is_valid_password(str(n), False)]
    print(f"There are {len(new_valid_passwords)} new valid passwords")


def pad_password(password):
    return "0" * (6 - len(password)) + password


def is_valid_password(password, allow_big_groups=True):
    padded_password = pad_password(password)
    has_double = False
    prev_char = "-1"
    group_length = 1
    for i in range(0, 6):
        char = padded_password[i]
        if int(char) < int(prev_char):
            return False
        if char == prev_char:
            group_length += 1
        if i == 5 or char != prev_char:
            if group_length == 2 or (allow_big_groups and group_length >= 2):
                has_double = True
            group_length = 1
        prev_char = char
    return has_double


if __name__ == "__main__":
    main()
