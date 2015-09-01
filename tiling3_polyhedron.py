from tiling3 import tiling3
from tau import tau
from vector3 import Vector3, triangle3_area, tetra3_volume

def tiling3_convex_hull(vertices, epsilon=1e-7):
    """
    Takes a dictionary of vertices, and creates a polyhedron given by
    the convex hull.
    """
    vertices = dict(vertices)
    l_vertices = list(vertices)
    n = len(vertices)
    faces = []

    def coplanar(i,j,k):
        """
        Find the vertices in the same plane as vertices i,j,k.

        At the beginning, we bale out if these vertices already lie in
        some face we've constructed already, and if the vertices are
        collinear.

        We calculate by considering the volume of the tetrahedron
        formed by vertices i,j,k and one other. If (close to) zero,
        the four points are coplanar. If positive, the other point is
        on one side of the plane, and if negative it's on the
        other. Hence we bale out if we find points on both sides of
        the plane.
        """
        level = set([i,j,k])

        if any(level.issubset(s) for s in faces):
            return None

        u = l_vertices[i]
        v = l_vertices[j]
        w = l_vertices[k]

        if abs(triangle3_area(u,v,w)) < epsilon:
            return None

        side1 = False
        side2 = False
        for r in range(0,i)+range(i+1,j)+range(j+1,k)+range(k+1,n):
            x = l_vertices[r]
            a = tetra3_volume(u,v,w,x)
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

    # Produce the faces: they're the maximal subsets of coplanar
    # vertices, with the property that every other vertex is on the
    # same side.
    for i in xrange(n-2):
        for j in xrange(i+1,n-1):
            for k in xrange(j+1,n):
                level = coplanar(i,j,k)
                if level is not None:
                    faces.append(level)
    faces = [frozenset(vertices[l_vertices[i]] for i in l) for l in faces]

    # The edges are the intersections of the faces that have size 2
    edges = set()
    n = len(faces)
    for i in xrange(0,n-1):
        for j in xrange(i+1,n):
            a = faces[i].intersection(faces[j])
            if len(a) == 2:
                edges.add(a)

    # Now we need the rest of the data in the preferred form
    volumes = [faces]
    faces = [set(e for e in edges if e.issubset(f)) for f in faces]
    vertices = dict((v,k) for (k,v) in vertices.iteritems())
    return tiling3(vertices, edges, faces, volumes)


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

regular_polytopes_3d = {'tetrahedron': tetrahedron(), 'cube':cube(), 'octahedron' : octahedron(), 
                         'dodecahedron': dodecahedron(), 'icosahedron' : icosahedron()}
