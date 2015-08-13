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
        '''
        Produces outputs of the form that should be valid inputs for the tiling3 function.
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

        return "tiling3(%r, %r, %r, %r)"%(dict_vertices, list_of_edges, list_of_faces, list_of_volumes)

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

    def map(self, v, e, f, g):
        """
        Adjust the labelling by v, e, f and g (on vertices, edges,
        faces and volumes respectively).
        """
        vertices = dict((x,v(l)) for (x,l) in self.vertices.iteritems())
        edges = dict((x,e(l)) for (x,l) in self.edges.iteritems())
        faces = dict((x,f(l)) for (x,l) in self.faces.iteritems())
        volumes = dict((x,g(l)) for (x,l) in self.volumes.iteritems())
        return Tiling3(vertices, edges, faces, volumes)

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
        return self.vertices == other.vertices and self.edges == other.edges and self.faces == other.faces and self.volumes == other.volumes

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

        inv = {}
        for (g,lg) in self.volumes.iteritems():
            volume_inv = {}
            for f in g:
                face_inv = faces[f]
                volume_inv[face_inv] = 1 + volume_inv.get(face_inv, 0)
            volume_inv = (tuple(sorted(volume_inv.iteritems())), lg)
            inv[volume_inv] = 1 + inv.get(volume_inv, 0)
        return tuple(sorted(inv.iteritems()))


def tiling3(dict_vertices, list_edges, list_faces, list_volumes):
    """
    This function is designed to help make Tiling3 objects
    corresponding to polyhedra.

    dict_vertices should be a dictionary with Vector3 objects
    as values.

    list_edges should be a list of lists where each sublists contains
    two labels of vertices which corresponds to the edge defined by
    joining those vertices; similarly for list_faces and list_volumes.
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

    volumes = {}
    for volume in list_volumes:
        s = frozenset(v for f in volume for v in f)
        volumes[frozenset(dict_faces[frozenset(k)] for k in volume)] = s

    # Now we reverse the keys and values to correct position for a tiling3 input.
    vertices = ((k,v) for (v,k) in dict_vertices.iteritems())
    edges = ((k,v) for (v,k) in dict_edges.iteritems())
    faces = ((k,v) for (v,k) in dict_faces.iteritems())

    return Tiling3(vertices, edges, faces, volumes)
