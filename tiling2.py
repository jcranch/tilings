from math import floor, ceil

from common import cycle
from vector2 import Vector2


class Tiling2():
    """
    Base class for a 3D tiling.
    """
    
    def __init__(self, v=None, e=None, f=None):
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
            
    def minx(self):
        return min(v.x for v in self.vertices)
    
    def maxx(self):
        return max(v.x for v in self.vertices)
    
    def miny(self):
        return min(v.y for v in self.vertices)
    
    def maxy(self):
        return max(v.y for v in self.vertices)      
    
    def deform(self, h):
        """
        Applies an arbitrary function h to the vertices.
        """
        v = dict((a,(h(a),x))
                 for a in self.vertices.iteritems())
        e = dict((a,(frozenset(v[i][0] for i in a),x))
                 for a in self.edges.iteritems())
        f = dict((a,(frozenset(e[i][0] for i in a),x))
                 for a in self.faces.iteritems())
        return Tiling2(v.itervalues(),e.itervalues(),f.itervalues())
            
    def translate(self, offset):
        return self.deform(lambda x: x+offset)
            
    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def sort_out_duplicates(self, epsilon=0.000001):
        """
        Replace very close vertices by the same vertex.

        This is more efficient than before: we sort by x
        coordinate. In groups where the x coordinates are close, we
        sort by y coordinate. Consecutive pairs where that is also
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
            for j in xrange(1,len(ly)):
                if abs(ly[j-1].y-ly[j].y) < epsilon:
                    d[ly[j]] = d.get(ly[j-1],ly[j-1])
            i1 = i2
        return self.deform(lambda v: d.get(v,v))            

    def clip(self, minx, maxx, miny, maxy):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = dict((v,x) for (v,x) in self.vertices.iteritems() if minx <= v.x <= maxx and miny <= v.y <= maxy)
        newe = dict((e,x) for (e,x) in self.edges.iteritems() if any(v in newv for v in e))
        newf = dict((f,x) for (f,x) in self.faces.iteritems() if any(e in newe for e in f))
        return Tiling2(newv, newe, newf)

    def write_eps(self, f, psbox, geobox, facecol=lambda x:(1.0,1.0,1.0)):
        (gminx, gmaxx, gminy, gmaxy) = geobox
        (pminx, pmaxx, pminy, pmaxy) = psbox
        def coords(v):
            x = (v.x-gminx)*(pmaxx-pminx)/(gmaxx-gminx) + pminx
            y = (v.y-gminy)*(pmaxy-pminy)/(gmaxy-gminy) + pminy
            return "%f %f"%(x,y)
        f.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        f.write("%%%%BoundingBox: %d %d %d %d\n"%psbox)
        for (face,x) in self.faces.iteritems():
            f.write("gsave %f %f %f setrgbcolor "%(facecol(x)))
            for (i,v) in enumerate(cycle(face)):
                f.write(coords(v))
                if i == 0:
                    f.write(" moveto ")
                else:
                    f.write(" lineto ")
            f.write("closepath fill grestore\n")
        for (v1,v2) in self.edges:
            f.write("newpath " + coords(v1) + " moveto " + coords(v2) + " lineto stroke\n")

def big_union2(tilings, epsilon=0.000001):
    """
    Take a union of a collection of tilings. This should be avoided,
    as it's really slow.
    """
    v = {}
    e = {}
    f = {}
    for t in tilings:
        v.update(t.vertices)
        e.update(t.edges)
        f.update(t.faces)
    return Tiling2(v,e,f).sort_out_duplicates(epsilon)


