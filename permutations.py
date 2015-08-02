def permutations_with_sign(original):
    if len(original)==0:
        yield (1,())
    else:
        x = original[0]
        for (s,p) in permutations_with_sign(original[1:]):
            for i in xrange(len(original)):
                yield (s, p[:i] + (x,) + p[i:])
                s = -s

def all_permutations(original):
    for (s,p) in permutations_with_sign(original):
        yield p


def even_permutations(original):
    for (s,p) in permutations_with_sign(original):
        if s == 1:
            yield p
