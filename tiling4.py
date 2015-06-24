from vector4 import Vector4


class Tiling4():
    """
    Base class for a 4D tiling.
    """

    def __init__(self, v=None, e=None, f=None, g=None, h=None):
        if v is None:
            self.vertices = {}
        else:
            self.vertices = dict(v)
        if e is None:
            self.edges = {}
        else:
            self.edges = dict(e)
        if f is None:
            self.faces = {}
        else:
            self.faces = dict(f)
        if g is None:
            self.volumes = {}
        else:
            self.volumes = dict(g)
        if h is None:
            self.hypervolumes = {}
        else:
            self.hypervolumes = dict(h)

    def minw(self):
        return min(v.w for v in self.vertices)

    def maxw(self):
        return max(v.w for v in self.vertices)

    def minx(self):
        return min(v.x for v in self.vertices)

    def maxx(self):
        return max(v.x for v in self.vertices)

    def miny(self):
        return min(v.y for v in self.vertices)

    def maxy(self):
        return max(v.y for v in self.vertices)

    def minz(self):
        return min(v.z for v in self.vertices)

    def maxz(self):
        return max(v.z for v in self.vertices)

    def deform(self, q):
        """
        Applies an arbitrary function q to the vertices.
        """
        v = dict((a,(h(a),x))
                 for (a,x) in self.vertices.iteritems())
        e = dict((a,(frozenset(v[i][0] for i in a), x))
                 for (a,x) in self.edges.iteritems())
        f = dict((a,(frozenset(e[i][0] for i in a), x))
                 for (a,x) in self.faces.iteritems())
        g = dict((a,(frozenset(f[i][0] for i in a), x))
                 for (a,x) in self.volumes.iteritems())
        h = dict((a,(frozenset(g[i][0] for i in a), x))
                 for (a,x) in self.hypervolumes.iteritems())
        return Tiling4(v.itervalues(), e.itervalues(), f.itervalues(), g.itervalues(), h.itervalues())

    def translate(self, offset):
        return self.deform(lambda x: x+offset)

    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def transform(self, matrix):
        return self.deform(matrix) # matrix action is overloaded function call

    def clip(self, minw, maxw, minx, maxx, miny, maxy, minz, maxz):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = dict((v,x) for (v,x) in self.vertices.iteritems() if minw <= v.w <= maxw and minx <= v.x <= maxx and miny <= v.y <= maxy and minz <= v.z <= maxz)
        newe = dict((e,x) for (e,x) in self.edges.iteritems() if any(v in newv for v in e))
        newf = dict((f,x) for (f,x) in self.faces.iteritems() if any(e in newe for e in f))
        newg = dict((g,x) for (g,x) in self.volumes.iteritems() if any(f in newf for f in g))
        newh = dict((h,x) for (h,x) in self.hypervolumes.iteritems() if any(g in newg for g in h))
        return Tiling4(newv, newe, newf, newg, newh)
