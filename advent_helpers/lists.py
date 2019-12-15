def get_permutations_of_list(l):
    if (len(l)) == 0:
        return [[]]
    else:
        return [[l[i]] + tail for i in range(len(l)) for tail in get_permutations_of_list(l[:i] + l[i + 1:])]
