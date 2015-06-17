

def cycle(f):
    """
    Given a cycle graph, given as an iterable collection of pairs of
    vertices, return the vertices in order.

    This is quadratic in the length of the cycle, so not the best
    algorithm possible, but it doesn't matter for now.
    """
    f = set(f)
    e = f.pop()
    while f:
        for e2 in f:
            i = e.intersection(e2)
            if i:
                v = next(iter(i))
                e = e2
                f.remove(e)
                yield v
                break
    for u in e:
        if u != v:
            yield u
    
