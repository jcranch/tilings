from math import floor, ceil


class Tiling1():
    """
    Base class for a 1D tiling.
    """
    
    def __init__(self, v=None, e=None):
        if v is None:
            self.vertices = {}
        else:
            self.vertices = dict(v)
        if e is None:
            self.edges = {}
        else:
            self.edges = dict(e)
            
    def minx(self):
        return min(self.vertices)
    
    def maxx(self):
        return max(self.vertices)
    
    def deform(self, h):
        """
        Applies an arbitrary function h to the vertices.
        """
        v = dict((a,(h(a),x))
                 for a in self.vertices.iteritems())
        e = dict((a,(frozenset(v[i][0] for i in a),x))
                 for a in self.edges.iteritems())
        return Tiling1(v.itervalues(),e.itervalues())
            
    def translate(self, offset):
        return self.deform(lambda x: x+offset)
            
    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def clip(self, minx, maxx):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = dict((v,x) for (v,x) in self.vertices.iteritems() if minx <= v.x <= maxx)
        newe = dict((e,x) for (e,x) in self.edges.iteritems() if any(v in newv for v in e))
        return Tiling1(newv, newe)


