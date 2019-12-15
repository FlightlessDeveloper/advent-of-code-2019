from itertools import count


def generate_primes():
    generated = set()
    for i in count(2):
        if all(i % j != 0 for j in generated):
            yield i
            generated.add(i)
