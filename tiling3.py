from vector3 import Vector3


class Tiling3():
    """
    Base class for a 3D tiling.
    """
    
    def __init__(self, v=None, e=None, f=None, g=None):
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

    def deform(self, h):
        """
        Applies an arbitrary function h to the vertices.
        """
        v = dict((a,(h(a),x))
                 for (a,x) in self.vertices.iteritems())
        e = dict((a,(frozenset(v[i][0] for i in a), x))
                 for (a,x) in self.edges.iteritems())
        f = dict((a,(frozenset(e[i][0] for i in a), x))
                 for (a,x) in self.faces.iteritems())
        g = dict((a,(frozenset(f[i][0] for i in a), x))
                 for (a,x) in self.volumes.iteritems())
        return Tiling3(v.itervalues(), e.itervalues(), f.itervalues(), g.itervalues())
            
    def translate(self, offset):
        return self.deform(lambda x: x+offset)
            
    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def transform(self, matrix):
        return self.deform(matrix) # matrix action is overloaded function call

    def sort_out_duplicates(self, epsilon=0.000001):
        """
        Replace very close vertices by the same vertex.

        This is more efficient than before: we sort by x
        coordinate. In groups where the x coordinates are close, we
        sort by y coordinate. In groups where that too is close, we
        sort by z coordinate. Consecutive pairs where that is again
        close are identified.
        """
        lx = sorted(self.vertices, key=lambda v:v.x)
        d = {}
        i1 = 0
        while i1 < len(lx):
            i2 = i1+1
            while i2 < len(lx) and abs(lx[i2-1].x-lx[i2].x) < epsilon:
                i2 += 1
            ly = sorted(lx[i1:i2], key=lambda v:v.y)
            j1 = 0
            while j1 < len(ly):
                j2 = j1+1
                while j2 < len(ly) and abs(ly[j2-1].y-ly[j2].y) < epsilon:
                    j2 += 1
                lz = sorted(ly[j1:j2], key=lambda v:v.z)
                for k in xrange(1,len(lz)):
                    if abs(lz[k-1].z-lz[k].z) < epsilon:
                        d[lz[k]] = d.get(lz[k-1],lz[k-1])
                j1 = j2
            i1 = i2
        return self.deform(lambda v: d.get(v,v))            

    def clip(self, minx, maxx, miny, maxy, minz, maxz):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = dict((v,x) for (v,x) in self.vertices.iteritems() if minx <= v.x <= maxx and miny <= v.y <= maxy and minz <= v.z <= maxz)
        newe = dict((e,x) for (e,x) in self.edges.iteritems() if any(v in newv for v in e))
        newf = dict((f,x) for (f,x) in self.faces.iteritems() if any(e in newe for e in f))
        newg = dict((g,x) for (g,x) in self.volumes.iteritems() if any(f in newf for f in g))
        return Tiling3(newv, newe, newf, newg)


def big_union3(tilings, epsilon=0.000001):
    """
    Take a union of a collection of tilings. This should be avoided,
    as it's really slow.
    """
    v = {}
    e = {}
    f = {}
    g = {}
    for t in tilings:
        v.update(t.vertices)
        e.update(t.edges)
        f.update(t.faces)
        g.update(t.volumes)
    return Tiling3(v,e,f,g).sort_out_duplicates(epsilon)
