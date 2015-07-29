from tiling3 import Tiling3
from tau import tau
from vector3 import Vector3, tetra_volume



def tiling3_polyhedron(dict_vertices, list_edges, list_faces, list_volumes):
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
    list_edges = list(list_edges)
    list_faces = list(list_faces)
    list_volumes = list(list_volumes)
    
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


def tiling3_convex_hull(vertices, epsilon=1e-7):
    """
    Takes a dictionary of vertices, and creates a polyhedron given by
    the convex hull.
    """
    vertices = dict(vertices)
    l_vertices = list(vertices)

    def coplanar(i,j,k):
        """
        Find the vertices in the same plane as vertices i,j,k.
        If any occur before k, then we bale out as we should have
        already considered this plane.

        We calculate by considering the volume of the tetrahedron
        formed by vertices i,j,k and one other. If (close to) zero,
        the four points are coplanar. If positive, the other point is
        on one side of the plane, and if negative it's on the
        other. Hence we bale out if we find points on both sides of
        the plane.
        """
        u = l_vertices[i]
        v = l_vertices[j]
        w = l_vertices[k]        
        side1 = False
        side2 = False
        for r in range(0,i)+range(i+1,j)+range(j+1,k):
            x = l_vertices[r]
            a = tetra_volume(u,v,w,x)
            if abs(tetra_volume(u,v,w,x)) < epsilon:
                return None
            elif a < 0:
                if side2:
                    return None
                side1 = True
            else:
                if side1:
                    return None
                side2 = True
        level = [u,v,w]
        for r in range(k+1,n):
            x = l_vertices[r]
            a = tetra_volume(u,v,w,x)
            if abs(tetra_volume(u,v,w,x)) < epsilon:
                level.append(x)
            elif a < 0:
                if side2:
                    return None
                side1 = True
            else:
                if side1:
                    return None
                side2 = True
        return level
    
    # Produce the faces: they're the maximal subsets of coplanar
    # vertices, with the property that every other vertex is on the
    # same side.
    n = len(l_vertices)
    faces = []
    for i in xrange(n-2):
        for j in xrange(i+1,n-1):
            for k in xrange(j+1,n):
                level = coplanar(i,j,k)
                if level is None:
                    continue
                faces.append(frozenset(level))

    # The edges are the intersections of the faces that have size 2
    edges = set()
    n = len(faces)
    for i in xrange(0,n-1):
        for j in xrange(i+1,n):
            a = faces[i].intersection(faces[j])
            if len(a) == 2:
                edges.add(a)

    # Now we need the rest of the data in the preferred form
    edges = [frozenset(vertices[v] for v in e) for e in edges]
    faces = [frozenset(vertices[v] for v in f) for f in faces]
    volumes = [faces]
    faces = [set(e for e in edges if e.issubset(f)) for f in faces]
    vertices = dict((v,k) for (k,v) in vertices.iteritems())
    return tiling3_polyhedron(vertices, edges, faces, volumes)

        
def tetrahedron():
    d = {Vector3(-1,-1,-1): 1,
         Vector3(-1,1,1): 2,
         Vector3(1,-1,1): 3,
         Vector3(1,1,-1): 4}
    return tiling3_convex_hull(d)

def cube():
    vertices = [Vector3(x,y,z)
                for x in [-1,1]
                for y in [-1,1]
                for z in [-1,1]]
    return tiling3_convex_hull(dict(zip(vertices,xrange(8))))

def octahedron():
    d = {Vector3(1,0,0): 1,
         Vector3(-1,0,0): 2,
         Vector3(0,1,0): 3,
         Vector3(0,-1,0): 4,
         Vector3(0,0,1): 5,
         Vector3(0,0,-1): 6}
    return tiling3_convex_hull(d)

def dodecahedron():
    vertices1 = [Vector3(x,y,z)
                 for x in [-1,1] for y in [-1,1] for z in [-1,1]]
    vertices2 = [v
                 for p in [tau, -tau]
                 for q in [tau.conj(), -tau.conj()]
                 for v in [Vector3(p,q,0), Vector3(q,0,p), Vector3(0,p,q)]]
    return tiling3_convex_hull(dict(zip(vertices1+vertices2,xrange(20))))    

def icosahedron():
    vertices = [v
                for p in [1,-1]
                for q in [tau, -tau]
                for v in [Vector3(p,q,0), Vector3(q,0,p), Vector3(0,p,q)]]
    return tiling3_convex_hull(dict(zip(vertices,xrange(12))))
