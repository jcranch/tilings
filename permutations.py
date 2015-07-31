def all_permutations(original):
    if len(original)==0:
        yield []
    else:
        x = original[0]
        for i in xrange(len(original)):
            for p in all_permutations(original[1:]):
                yield p[:i] + [x] + p[i:]
  

def cycle_decomposition(permutation, original=None):
    if original is None:
        original = sorted(permutation)
    d = dict(zip(original,permutation))
    remaining = set(original)
    while remaining:
        x = remaining.pop()
        current = [x]
        x = d[x]
        while x in remaining:
            remaining.remove(x)
            current.append(x)
            x = d[x]
        yield current


def permutation_parity(permutation, original=None):
    cycles = cycle_decomposition(permutation, original)
    sgn = 1
    for cycle in cycles:
        if len(cycle)%2 == 0:
            sgn = -sgn
    return sgn


def even_permutations(original):
    for p in all_permutations(original):
        if permutation_parity(p,original)==1:
            yield p


def perform_permutation(permutable, permutation, original=None): #cycle of the form [1,2,3,4]
    if original is None:
        original = sorted(permutation)
    d = dict(zip(original,permutation))
    return [d[x] for x in permutable]
    

def produce_permutable_plus_minus(permutable):
    '''
    Performs a given permutation on all in  set (+- a, +- b, +- c, +- d).
    '''
    list_of_results = []
    for sgn1 in [-1,1]:
        for sgn2 in [-1,1]:
            for sgn3 in [-1,1]:
                for sgn4 in [-1,1]:
                    considered_permutable = [permutable[0]*sgn1,permutable[1]*sgn2,permutable[2]*sgn3,permutable[3]*sgn4]
                    list_of_results += [considered_permutable]
    return list_of_results


def perform_multiple_permutations_on_multible_permutables(list_of_permutables, list_of_permutations):
    list_of_results = []
    for permutable in list_of_permutables:
        for permutation in list_of_permutations:
            list_of_results += [perform_permutation(permutable, permutation)]
    return list_of_results
