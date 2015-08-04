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
