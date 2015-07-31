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

    def __repr__(self):
        return "Tiling3(%r, %r, %r, %r)"%(self.vertices, self.edges, self.faces, self.volumes)

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

        It's still slow.
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

    def write_eps(self, f, psbox, geobox,
                  subdivs=20,
                  zcontribx=0.708,
                  zcontriby=0.318,
                  edgecol=lambda x:(0.0, 0.0, 0.0),
                  width1=3.0,
                  whiterange=10.0):
        """
        Draw a picture of an orthographic projection of the edges, in
        EPS format, coloured so as to fade to white in the distance

        Arguments:
         - f is a file object
         - psbox is the coordinates of the box in the output
           PostScript
         - geobox is the coordinates of the corresponding box in the
           Tiling2
         - subdivs is the number of subdivisions of each edge (the
           more the smoother)
         - zcontribx and zcontriby
         - edgecol takes the label of an edge, and returns the desired
           colour (in RGB format, between 0.0 and 1.0).
         - whiterange is the value of the z coordinate at which things
           become completely white.

        Note that the order of the coordinates for psbox and geobox is
        different!
        """

        (gminx, gmaxx, gminy, gmaxy) = geobox
        (pminx, pminy, pmaxx, pmaxy) = psbox

        def coords(v):
            x1 = v.x + zcontribx * v.z
            y1 = v.y + zcontriby * v.z
            x = (x1-gminx)*(pmaxx-pminx)/(gmaxx-gminx) + pminx
            y = (y1-gminy)*(pmaxy-pminy)/(gmaxy-gminy) + pminy
            return (x,y)

        def edgelets():
            for ((v1,v2),x) in self.edges.iteritems():
                if v1.z < v2.z:
                    (v1,v2) = (v2,v1)
                if v1.z < 0:
                    continue
                for i in xrange(subdivs):
                    # start and end of edgelets
                    t1 = float(i)/subdivs
                    u1 = v1*t1 + v2*(1-t1)
                    t2 = float(i+1)/subdivs
                    u2 = v1*t2 + v2*(1-t2)

                    if u2.z < 0:
                        continue

                    # colour, whitening it into the distance
                    (r,g,b) = edgecol(x)
                    w = max(min(u1.z/whiterange, 1.0), 0.0)
                    (r,g,b) = (w + (1-w)*r, w + (1-w)*g, w + (1-w)*b)

                    # line thickness
                    t = width1/u1.z

                    yield (u1, u2, (r,g,b), t)

        f.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        f.write("%%%%BoundingBox: %d %d %d %d\n\n"%psbox)
        for (u1, u2, (r, g, b), t) in sorted(edgelets(), key=lambda t:-(t[0].z)):
            (x1,y1) = coords(u1)
            (x2,y2) = coords(u2)
            if x1 < pminx and x2 < pminx:
                continue
            if x1 > pmaxx and x2 > pmaxx:
                continue
            if y1 < pminy and y2 < pminy:
                continue
            if y1 > pmaxy and y2 > pmaxy:
                continue
            f.write("gsave %f %f %f setrgbcolor %f setlinewidth newpath %f %f moveto %f %f lineto stroke grestore\n"%(r,g,b,t,x1,y1,x2,y2))


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
