import argparse


WIDTH = 25
HEIGHT = 6


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    return parser.parse_args()


def main():
    args = parse_args()
    raw_image = [int(x) for x in ([x for x in open(args.input_file)][0]) if '0' <= x <= '9']
    image = [[[raw_image[(layer * WIDTH * HEIGHT) + (row * WIDTH) + column]
               for column in range(WIDTH)] for row in range(HEIGHT)]
             for layer in range(0, len(raw_image) // (WIDTH * HEIGHT))]

    layer_lowest_zeroes = find_layer_with_fewest_zeros(image)
    checksum = count_in_layer(layer_lowest_zeroes, 1) * count_in_layer(layer_lowest_zeroes, 2)
    print(f"Checksum: {checksum}")
    print(image_to_string(image))


def find_layer_with_fewest_zeros(layers):
    lowest_num_zeroes = WIDTH + HEIGHT
    lowest_num_zeroes_layer = []
    for layer in layers:
        num_zeroes = count_in_layer(layer, 0)
        if num_zeroes < lowest_num_zeroes:
            lowest_num_zeroes = num_zeroes
            lowest_num_zeroes_layer = layer
    return lowest_num_zeroes_layer


def image_to_string(image):
    image_string = [['*' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for row in range(WIDTH):
        for col in range(HEIGHT):
            for layer in image:
                pixel = layer[col][row]
                if pixel != 2:
                    image_string[col][row] = pixel_to_char(pixel)
                    break
    return "\n".join("".join(pixel for pixel in row) for row in image_string)


def pixel_to_char(pixel):
    if pixel == 0:
        return ' '
    elif pixel == 1:
        return '#'
    else:
        raise Exception(f"Invalid pixel: '{pixel}'")


def count_in_layer(layer, target):
    return len([pixel for row in layer for pixel in row if pixel == target])


if __name__ == "__main__":
    main()
