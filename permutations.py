def permutations_with_sign(original):
    if len(original)==0:
        yield (1,())
    else:
        x = original[0]
        for (s,p) in permutations_with_sign(original[1:]):
            for i in range(len(original)):
                yield (s, p[:i] + (x,) + p[i:])
                s = -s

def all_permutations(original):
    for (s,p) in permutations_with_sign(original):
        yield p


def even_permutations(original):
    for (s,p) in permutations_with_sign(original):
        if s == 1:
            yield p

def plus_minuses(original):
    """
    All combinations of plus or minus the components.
    """
    if len(original)==0:
        yield ()
    else:
        r = original[0]
        rs = original[1:]
        for x in set([r,-r]):
            for xs in plus_minuses(rs):
                yield (x,) + xs

def all_permutations_plus_minus(original):
    for a in plus_minuses(original):
        for p in all_permutations(a):
            yield p

def even_permutations_plus_minus(original):
    for a in plus_minuses(original):
        for p in even_permutations(a):
            yield p
