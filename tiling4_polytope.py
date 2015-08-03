from tiling4 import Tiling4
from vector4 import Vector4
from matrix4 import tetra4_volume, pentatope4_hypervolume
from permutations import plus_minuses


def tiling4_polytope(dict_vertices, list_edges, list_faces, list_volumes, list_hypervolumes):
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


def tiling4_convex_hull(vertices, epsilon=1e-7, statusreport=False):
    """
    Takes a dictionary of vertices, and creates a polyhedron given by
    the convex hull.
    """
    vertices = dict(vertices)
    l_vertices = list(vertices)
    n = len(l_vertices)
    volumes = []

    def cohyperplanar(h,i,j,k):
        """
        Find the vertices in the same hyperplane as vertices h,i,j,k.

        At the beginning, we bale out if these vertices already lie in
        some volume we've constructed already, and if the vertices are
        in fact coplanar.

        We calculate by considering the hypervolume of the pentatope
        formed by vertices h,i,j,k and one other. If (close to) zero,
        the five points are cohyperplanar. If positive, the other point is
        on one side of the cell, and if negative it's on the
        other. We bale out if we find points on both sides of the cell.
        """
        level = set([h,i,j,k])

        if any(level.issubset(s) for s in volumes):
            return None

        t = l_vertices[h]
        u = l_vertices[i]
        v = l_vertices[j]
        w = l_vertices[k]

        if abs(tetra4_volume(t,u,v,w)) < epsilon:
            return None

        side1 = False
        side2 = False
        for r in range(0,h)+range(h+1,i)+range(i+1,j)+range(j+1,k)+range(k+1,n):
            x = l_vertices[r]
            a = pentatope4_hypervolume(t,u,v,w,x)
            if abs(a) < epsilon:
                level.add(r)
            elif a < 0:
                if side2:
                    return None
                side1 = True
            else:
                if side1:
                    return None
                side2 = True
        return level

    # Produce the volumes: they're the maximal subsets of cohyperplanar
    # vertices, with the property that every other vertex is on the
    # same side.
    for h in xrange(n-3):
        for i in xrange(h+1,n-2):
            for j in xrange(i+1,n-1):
                for k in xrange(j+1,n):
                    level = cohyperplanar(h,i,j,k)
                    if level is not None:
                        volumes.append(level)
                        if statusreport:
                            print "  found %d volumes"%(len(volumes),)
    volumes = [frozenset(vertices[l_vertices[i]] for i in l) for l in volumes]

    # The faces are the intersections of the volumes that have at
    # least 3 vertices in common, and the edges are those that have
    # two vertices in common.
    faces = set()
    n = len(volumes)
    for i in xrange(0,n-1):
        for j in xrange(i+1,n):
            a = volumes[i].intersection(volumes[j])
            if len(a) > 2:
                faces.add(a)

    edges = set()
    lfaces = list(faces)
    n = len(lfaces)
    for i in xrange(0,n-1):
        for j in xrange(i+1,n):
            a = lfaces[i].intersection(lfaces[j])
            if len(a) == 2:
                edges.add(a)

    # Now we need the rest of the data in the preferred form
    hypervolumes = [volumes]
    volumes = [set(f for f in faces if f.issubset(g)) for g in volumes]
    faces = [set(e for e in edges if e.issubset(f)) for f in faces]
    vertices = dict((v,k) for (k,v) in vertices.iteritems())
    return tiling4_polytope(vertices, edges, faces, volumes, hypervolumes)


def pentatope():
    root5 = 5**0.5
    dictionary_of_vertices = {
        Vector4(1, 1, 1, -1/root5): 0,
        Vector4(1, -1, -1, -1/root5): 1,
        Vector4(-1, 1, -1, -1/root5): 2,
        Vector4(-1, -1, 1, -1/root5): 3,
        Vector4(0, 0, 0, root5 - 1/root5): 4 }
    return tiling4_convex_hull(dictionary_of_vertices)

def hypercube():
    vertices = [Vector4(w,x,y,z) for (w,x,y,z) in plus_minuses([1,1,1,1])]
    return tiling4_convex_hull(dict(zip(vertices,xrange(16))))

def cell16():
    dictionary_of_vertices = {
        Vector4(1, 0, 0, 0): 0,
        Vector4(0, 1, 0, 0): 1,
        Vector4(0, 0, 1, 0): 2,
        Vector4(0, 0, 0, 1): 3,
        Vector4(-1, 0, 0, 0): 4,
        Vector4(0, -1, 0, 0): 5,
        Vector4(0, 0, -1, 0): 6,
        Vector4(0, 0, 0, -1): 7 }
    return tiling4_convex_hull(dictionary_of_vertices)

def cell24():
    with open("autotilings/cell24.data", 'r') as f:
        return(eval(f.read()))

def cell120():
    with open("autotilings/cell120.data", 'r') as f:
        return(eval(f.read()))

def cell600():
    with open("autotilings/cell600.data", 'r') as f:
        return(eval(f.read()))

