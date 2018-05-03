class EquivDict(dict):
    """
    A version of a dict designed for unhashable keys, or keys intended
    to be considered up to some weaker equivalence relation than
    equality.
    """

    def __init__(self, contents=(),
                 invariant=lambda x:None,
                 equiv=lambda x,y:x==y):

        self.invariant = invariant
        self.equiv = equiv
        self.underlying = {}
        
        if isinstance(contents, dict):
            contents = contents.items()
            for (k,v) in contents:
                self[k] = v

    def __nonzero__(self):
        return any(a for a in self.underlying.values())
                
    def __len__(self):
        return sum(len(a) for a in self.underlying.values())

    def __getitem__(self, k):
        for (k1,v1) in self.underlying[self.invariant(k)]:
            if self.equiv(k, k1):
                return v1
        raise KeyError(k)
                
    def __setitem__(self, k, v):
        inv = self.invariant(k)
        if inv in self.underlying:
            a = self.underlying[inv]
        else:
            a = []
            self.underlying[inv] = a
        for (i, (k1,v1)) in enumerate(a):
            if self.equiv(k, k1):
                a[i] = (k, v)
                return None
        a.append((k, v))

    def iterkeys(self):
        for a in self.underlying.values():
            for (k,v) in a:
                yield k

    def itervalues(self):
        for a in self.underlying.values():
            for (k,v) in a:
                yield k

    def iteritems(self):
        for a in self.underlying.values():
            for t in a:
                yield t
