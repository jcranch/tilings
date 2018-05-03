from math import floor, ceil

from common import cycle
from vector2 import Vector2


class Tiling2(object):
    """
    Base class for a 2D tiling.
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

    def __repr__(self):
        return "Tiling2(%r, %r, %r)"%(self.vertices, self.edges, self.faces)

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
                 for (a,x) in self.vertices.items())
        e = dict((a,(frozenset(v[i][0] for i in a),x))
                 for (a,x) in self.edges.items())
        f = dict((a,(frozenset(e[i][0] for i in a),x))
                 for (a,x) in self.faces.items())
        return Tiling2(v.values(),e.values(),f.values())

    def translate(self, offset):
        return self.deform(lambda x: x+offset)

    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def transform(self, matrix):
        return self.deform(matrix) # matrix action is overloaded function call

    def in_box(self, box):
        ((minx, maxx), (miny, maxy)) = box
        return (minx <= self.minx() and self.maxx() <= maxx and
                miny <= self.miny() and self.maxy() <= maxy)
    
    def clip(self, minx, maxx, miny, maxy):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = dict((v,x) for (v,x) in self.vertices.items() if minx <= v.x <= maxx and miny <= v.y <= maxy)
        newe = dict((e,x) for (e,x) in self.edges.items() if any(v in newv for v in e))
        newf = dict((f,x) for (f,x) in self.faces.items() if any(e in newe for e in f))
        return Tiling2(newv, newe, newf)

    def write_eps(self, f, psbox, geobox, facecol=lambda x:(1.0,1.0,1.0)):
        """
        Draw a picture in EPS format.

        Arguments:
         - f is a file object
         - psbox is the coordinates of the box in the output
           PostScript
         - geobox is the coordinates of the corresponding box in the
           Tiling2
         - facecol takes the label of a face, and returns the desired
           colour (in RGB format, between 0.0 and 1.0).

        Note that the order of the coordinates for psbox and geobox is
        different!
        """
        (gminx, gmaxx, gminy, gmaxy) = geobox
        (pminx, pminy, pmaxx, pmaxy) = psbox
        def coords(v):
            x = (v.x-gminx)*(pmaxx-pminx)/(gmaxx-gminx) + pminx
            y = (v.y-gminy)*(pmaxy-pminy)/(gmaxy-gminy) + pminy
            return "%f %f"%(x,y)
        f.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        f.write("%%%%BoundingBox: %d %d %d %d\n"%psbox)
        for (face,x) in self.faces.items():
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

    def face_count_information(self):
        polygon_count = {}
        for face in self.faces.keys():
            n = len(face)
            if n not in polygon_count.keys() :
                polygon_count[n] = 1
            else:
                polygon_count[n] += 1
        return polygon_count

    def face_count_information_print(self):
        for (k,v) in polygon_count(self).items():
            print('Number of %s_gons : %s.'%(k,v))

    def map(self, v, e, f):
        """
        Adjust the labelling by v, e and f (on vertices, edges and
        faces respectively).
        """
        vertices = dict((x,v(l)) for (x,l) in self.vertices.items())
        edges = dict((x,e(l)) for (x,l) in self.edges.items())
        faces = dict((x,f(l)) for (x,l) in self.faces.items())
        return Tiling2(vertices, edges, faces)

    def isometries(self, other, epsilon=1e-7):
        """
        Generates dicts from the vertices of self to the vertices of
        other which are isometries (ie. preserve distances within
        epsilon) and preserve labelling.
        """
        vertices = list(self.vertices.items())

        def extensions(i, d):
            if i==len(vertices):
                yield d
            else:
                (v1,l1) = vertices[i]
                s = set(d.values())
                for (v2,l2) in other.vertices.items():
                    if v2 not in s and l1==l2 and all(abs(u1.distance(v1) - u2.distance(v2)) < epsilon for (u1,u2) in d.items()):
                        newd = d.copy()
                        newd[v1] = v2
                        for a in extensions(i+1, newd):
                            yield a

        if len(vertices)==len(other.vertices):
            for a in extensions(0, {}):
                yield a

    def isometric(self, other, epsilon=1e-7):
        """
        Are there any isometries between the two?
        """
        for i in self.isometries(other, epsilon):
            return True
        return False

    def __eq__(self, other):
        """
        Do they have identical structure? Use with care.
        """
        return self.vertices == other.vertices and self.edges == other.edges and self.faces == other.faces

    def isomorphisms(self, other):
        """
        Generates dicts from the vertices of self to the vertices of
        other which are isomorphisms (ie. preserve combinatorial
        structure, including labellings)
        """
        vertices = list(self.vertices.items())

        def extensions(i, d):
            if i==len(vertices):
                yield d
            else:
                (v1,l1) = vertices[i]
                s = set(d.values())
                for (v2,l2) in other.vertices.items():
                    if v2 not in s and l1==l2:
                        newd = d.copy()
                        newd[v1] = v2
                        news = set(newd.values())
                        def characteristic(x):
                            if x in news:
                                return x
                            else:
                                return None
                        edges1 = set((frozenset([newd.get(x), newd.get(y)]), l) for ((x,y),l) in self.edges.items())
                        edges2 = set((frozenset([characteristic(x), characteristic(y)]), l) for ((x,y),l) in other.edges.items())
                        if edges1 != edges2:
                            continue
                        faces1 = set((frozenset(frozenset(newd.get(v) for v in e) for e in f), l) for (f,l) in self.faces.items())
                        faces2 = set((frozenset(frozenset(characteristic(v) for v in e) for e in f), l) for (f,l) in other.faces.items())
                        if faces1 != faces2:
                            continue
                        for a in extensions(i+1, newd):
                            yield a

        if self.invariant()==other.invariant():
            for a in extensions(0, {}):
                yield a

    def isomorphic(self, other):
        """
        Are there any isomorphisms between the two?
        """
        for i in self.isomorphisms(other):
            return True
        return False

    def invariant(self):
        """
        A handy invariant, useful as a first step in deciding
        isomorphism.
        """

        edges = {}
        for (e,le) in self.edges.items():
            edge_inv = {}
            for v in e:
                vertex_inv = self.vertices[v]
                edge_inv[vertex_inv] = 1 + edge_inv.get(vertex_inv, 0)
            edges[e] = (tuple(sorted(edge_inv.items())), le)

        inv = {}
        for (f,lf) in self.faces.items():
            face_inv = {}
            for e in f:
                edge_inv = edges[e]
                face_inv[edge_inv] = 1 + face_inv.get(edge_inv, 0)
            face_inv = (tuple(sorted(face_inv.items())), lf)
            inv[face_inv] = 1 + inv.get(face_inv, 0)
        return tuple(sorted(inv.items()))

    def vertextour(self):
        """
        Generate the vertices, moving to the nearest at each stage: a
        greedy travelling postman.
        """
        s = set(self.vertices)
        x = s.pop()
        yield x
        while s:
            x = min(s, key=x.distance)
            s.remove(x)
            yield x

    def proximate(self, other, epsilon=1e-7):
        """
        Are these two almst identical: do they have they corresponding
        vertices within epsilon and corresponding higher structure?
        """
        if len(self.vertices) != len(other.vertices):
            return False
        if len(self.edges) != len(other.edges):
            return False
        if len(self.faces) != len(other.faces):
            return False
        d = {}
        for (u,x) in self.vertices.items():
            l = [v for (v,y) in other.vertices.items() if x==y and u.distance(v)<epsilon]
            if len(l) != 1:
                print((u,l))
                return False
            d[u] = l[0]
        for (e,x) in self.edges.items():
            e = frozenset(d[v] for v in e)
            if e not in other.edges or other.edges[e] != x:
                return False
        for (f,x) in self.faces.items():
            f = frozenset(frozenset(d[v] for v in e) for e in f)
            if f not in other.faces or other.faces[f] != x:
                return False
        return True
