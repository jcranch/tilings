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

def all_unique_permutation_plus_minus(original):
    permutables = []
    for sign1 in [-1,1]:
        for sign2 in [-1,1]:
            for sign3 in [-1,1]:
                for sign4 in [-1,1]:
                    p = [original[0]*sign1,original[1]*sign2,original[2]*sign3,original[3]*sign4]
                    if p not in permutables:
                        permutables += [p]

    vertices = []                    
    for p in permutables:
        for i in all_permutations(p):
            if i not in vertices:
                vertices += [i]
    return vertices

def only_even_unique_permutation_plus_minus(original):
    permutables = []
    for sign1 in [-1,1]:
        for sign2 in [-1,1]:
            for sign3 in [-1,1]:
                for sign4 in [-1,1]:
                    p = [original[0]*sign1,original[1]*sign2,original[2]*sign3,original[3]*sign4]
                    if p not in permutables:
                        permutables += [p]

    vertices = []                    
    for p in permutables:
        for i in even_permutations(p):
            if i not in vertices:
                vertices += [i]
    return vertices
