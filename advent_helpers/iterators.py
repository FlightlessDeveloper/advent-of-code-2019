from itertools import count


def get_permutations_of_list(l):
    if (len(l)) == 0:
        return [[]]
    else:
        return [[l[i]] + tail for i in range(len(l)) for tail in get_permutations_of_list(l[:i] + l[i + 1:])]


def take_until_duplicate(it):
    already_found = set()
    while True:
        next_value = next(it)
        if next_value in already_found:
            break
        yield next_value
        already_found.add(next_value)


def generate_primes():
    generated = set()
    for i in count(2):
        if all(i % j != 0 for j in generated):
            yield i
            generated.add(i)
