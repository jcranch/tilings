

class LatticeSearcher(object):
    """
    Helper class for generating bounded lattice vectors: it generates
    tuples of integers of length n, moving to neighbours of previously
    visited tuples, ignoring those where "reject" has been called.
    """

    def __init__(self, n):
        self.dim = n
        self.old = set()
        self.new = set([tuple(0 for i in range(n))])
        self.last = None

    def __iter__(self):
        return self

    def reject(self):
        self.last = None

    def __next__(self):
        if self.last is not None:
            a = self.last
            self.old.add(a)
            for i in range(self.dim):
                for x in [a[i]+1, a[i]-1]:
                    b = a[:i] + (x,) + a[(i+1):]
                    if b not in self.old:
                        self.new.add(b)
        if self.new:
            a = self.new.pop()
            self.last = a
            return a
        else:
            raise StopIteration


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


def remove_duplicates(g):
    s = set()
    for x in g:
        if x not in s:
            yield x
            s.add(x)
