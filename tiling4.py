from vector4 import Vector4


class Tiling4(object):
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

    def __repr__(self):
        '''
        Produces outputs of the form that should be valid inputs for the tiling4 function.
        '''
        dict_vertices = dict([(v,k) for(k,v) in self.vertices.iteritems()])

        list_of_edges = list()
        for i in self.edges.values():
            list_of_edges.append(frozenset(list(i)))
        set(list_of_edges)

        list_of_faces = list()
        for face in self.faces:
            list_of_edge = set()
            for edge in face:
                list_of_edge.add(self.edges[edge])
            list_of_faces.append(list_of_edge)

        list_of_volumes = list()
        for volume in self.volumes:
            list_of_face = set()
            for face in volume:
                list_of_face.add(self.faces[face])
            list_of_volumes.append(list_of_face)

        list_of_hypervolumes = list()
        for hypervolume in self.hypervolumes:
            list_of_volume = set()
            for volume in hypervolume:
                list_of_volume.add(self.volumes[volume])
            list_of_hypervolumes.append(list_of_volume)

        return "tiling4(%r, %r, %r, %r, %r)"%(dict_vertices, list_of_edges, list_of_faces, list_of_volumes, list_of_hypervolumes)

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
        v = dict((a,(q(a),x))
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

    def in_box(self, box):
        ((minw, maxw), (minx, maxx), (miny, maxy), (minz, maxz)) = box
        return (minw <= self.minw() and self.maxw() <= maxw and
                minx <= self.minx() and self.maxx() <= maxx and
                miny <= self.miny() and self.maxy() <= maxy and
                minz <= self.minz() and self.maxz() <= maxz)
    
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

    def map(self, v, e, f, g, h):
        """
        Adjust the labelling by v, e, f, g and h (on vertices, edges,
        faces and volumes respectively).
        """
        vertices = dict((x,v(l)) for (x,l) in self.vertices.iteritems())
        edges = dict((x,e(l)) for (x,l) in self.edges.iteritems())
        faces = dict((x,f(l)) for (x,l) in self.faces.iteritems())
        volumes = dict((x,g(l)) for (x,l) in self.volumes.iteritems())
        hypervolumes = dict((x,h(l)) for (x,l) in self.hypervolumes.iteritems())
        return Tiling4(vertices, edges, faces, volumes, hypervolumes)

    def isometries(self, other, epsilon=1e-7):
        """
        Generates dicts from the vertices of self to the vertices of
        other which are isometries (ie. preserve distances within
        epsilon) and preserve labelling.
        """
        vertices = list(self.vertices.iteritems())

        def extensions(i, d):
            if i==len(vertices):
                yield d
            else:
                (v1,l1) = vertices[i]
                s = set(d.itervalues())
                for (v2,l2) in other.vertices.iteritems():
                    if v2 not in s and l1==l2 and all(abs(u1.distance(v1) - u2.distance(v2)) < epsilon for (u1,u2) in d.iteritems()):
                        newd = d.copy()
                        newd[v1] = v2
                        for a in extensions(i+1, newd):
                            yield a

        if self.invariant()==other.invariant():
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
        return self.vertices == other.vertices and self.edges == other.edges and self.faces == other.faces and self.volumes == other.volumes and self.hypervolumes == other.hypervolumes

    def isomorphisms(self, other):
        """
        Generates dicts from the vertices of self to the vertices of
        other which are isomorphisms (ie. preserve combinatorial
        structure, including labellings)
        """
        vertices = list(self.vertices.iteritems())

        def extensions(i, d):
            if i==len(vertices):
                yield d
            else:
                (v1,l1) = vertices[i]
                s = set(d.itervalues())
                for (v2,l2) in other.vertices.iteritems():
                    if v2 not in s and l1==l2:
                        newd = d.copy()
                        newd[v1] = v2
                        news = set(newd.itervalues())
                        def characteristic(x):
                            if x in news:
                                return x
                            else:
                                return None
                        edges1 = set((frozenset([newd.get(x), newd.get(y)]), l) for ((x,y),l) in self.edges.iteritems())
                        edges2 = set((frozenset([characteristic(x), characteristic(y)]), l) for ((x,y),l) in other.edges.iteritems())
                        if edges1 != edges2:
                            continue
                        faces1 = set((frozenset(frozenset(newd.get(v) for v in e) for e in f), l) for (f,l) in self.faces.iteritems())
                        faces2 = set((frozenset(frozenset(characteristic(v) for v in e) for e in f), l) for (f,l) in other.faces.iteritems())
                        if faces1 != faces2:
                            continue
                        volumes1 = set((frozenset(frozenset(frozenset(newd.get(v) for v in e) for e in f) for f in g), l) for (g,l) in self.volumes.iteritems())
                        volumes2 = set((frozenset(frozenset(frozenset(characteristic(v) for v in e) for e in f) for f in g), l) for (g,l) in other.volumes.iteritems())
                        if volumes1 != volumes2:
                            continue
                        hypervolumes1 = set((frozenset(frozenset(frozenset(frozenset(newd.get(v) for v in e) for e in f) for f in g) for g in h), l) for (h,l) in self.hypervolumes.iteritems())
                        hypervolumes2 = set((frozenset(frozenset(frozenset(frozenset(characteristic(v) for v in e) for e in f) for f in g) for g in h), l) for (h,l) in other.hypervolumes.iteritems())
                        if hypervolumes1 != hypervolumes2:
                            continue
                        for a in extensions(i+1, newd):
                            yield a

        if len(vertices)==len(other.vertices):
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
        for (e,le) in self.edges.iteritems():
            edge_inv = {}
            for v in e:
                vertex_inv = self.vertices[v]
                edge_inv[vertex_inv] = 1 + edge_inv.get(vertex_inv, 0)
            edges[e] = (tuple(sorted(edge_inv.iteritems())), le)

        faces = {}
        for (f,lf) in self.faces.iteritems():
            face_inv = {}
            for e in f:
                edge_inv = edges[e]
                face_inv[edge_inv] = 1 + face_inv.get(edge_inv, 0)
            faces[f] = (tuple(sorted(face_inv.iteritems())), lf)

        volumes = {}
        for (g,lg) in self.volumes.iteritems():
            volume_inv = {}
            for f in g:
                face_inv = faces[f]
                volume_inv[face_inv] = 1 + volume_inv.get(face_inv, 0)
            volumes[g] = (tuple(sorted(volume_inv.iteritems())), lg)

        inv = {}
        for (h,lh) in self.hypervolumes.iteritems():
            hypervolume_inv = {}
            for g in h:
                volume_inv = volumes[g]
                hypervolume_inv[volume_inv] = 1 + hypervolume_inv.get(volume_inv, 0)
            hypervolume_inv = (tuple(sorted(hypervolume_inv.iteritems())), lh)
            inv[hypervolume_inv] = 1 + inv.get(hypervolume_inv, 0)
        return tuple(sorted(inv.iteritems()))

    def vertextour(self):
        """
        Generate the vertices, moving to the nearest at each stage: a
        greedy travelling postman. Useful for algorithms later.
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
        Are these two almost identical: do they have corresponding
        vertices within epsilon and corresponding higher structure?
        """
        if len(self.vertices) != len(other.vertices):
            return False
        if len(self.edges) != len(other.edges):
            return False
        if len(self.faces) != len(other.faces):
            return False
        if len(self.volumes) != len(other.volumes):
            return False
        if len(self.hypervolumes) != len(other.hypervolumes):
            return False
        d = {}
        for (u,x) in self.vertices.iteritems():
            l = [v for (v,y) in other.vertices.iteritems() if x==y and u.distance(v)<epsilon]
            if len(l) != 1:
                return False
            d[u] = l[0]
        for (e,x) in self.edges.iteritems():
            e = frozenset(d[v] for v in e)
            if e not in other.edges or other.edges[e] != x:
                return False
        for (f,x) in self.faces.iteritems():
            f = frozenset(frozenset(d[v] for v in e) for e in f)
            if f not in other.faces or other.faces[f] != x:
                return False
        for (g,x) in self.volumes.iteritems():
            g = frozenset(frozenset(frozenset(d[v] for v in e) for e in f) for f in g)
            if g not in other.volumes or other.volumes[g] != x:
                return False
        for (h,x) in self.hypervolumes.iteritems():
            h = frozenset(frozenset(frozenset(frozenset(d[v] for v in e) for e in f) for f in g) for g in h)
            if h not in other.hypervolumes or other.hypervolumes[h] != x:
                return False
        return True
            

def tiling4(dict_vertices, list_edges, list_faces, list_volumes, list_hypervolumes):
    """
    This function is designed to help make Tiling4 objects
    corresponding to polytopes.
    dict_vertices should be a dictionary with Vector4 objects
    as values.
    list_edges should be a list of lists where each sublists contains
    two labels of vertices which corresponds to the edge defined by
    joining those vertices; similarly for list_faces, list_volumes and list_hypervolumes.
    """
    dict_vertices = dict(dict_vertices)

    # We reverse the keys and values for now and change them at the end.
    dict_edges = {}
    for edge in list_edges:
        s = frozenset(edge)
        dict_edges[s] = frozenset(dict_vertices[k] for k in edge)

    dict_faces = {}
    for face in list_faces:
        s = frozenset(v for e in face for v in e)
        dict_faces[s] = frozenset(dict_edges[frozenset(k)] for k in face)

    dict_volumes = {}
    for volume in list_volumes:
        s = frozenset(v for f in volume for v in f)
        dict_volumes[s] = frozenset(dict_faces[frozenset(k)] for k in volume)

    hypervolumes = {}
    for hypervolume in list_hypervolumes:
        s = frozenset(v for g in hypervolume for v in g)
        hypervolumes[frozenset(dict_volumes[frozenset(k)] for k in hypervolume)] = s

    # Now we reverse the keys and values to correct position for a tiling4.
    vertices = ((k,v) for (v,k) in dict_vertices.iteritems())
    edges = ((k,v) for (v,k) in dict_edges.iteritems())
    faces = ((k,v) for (v,k) in dict_faces.iteritems())
    volumes = ((k,v) for (v,k) in dict_volumes.iteritems())

    return Tiling4(vertices, edges, faces, volumes, hypervolumes)
